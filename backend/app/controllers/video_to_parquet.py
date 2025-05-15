import logging

import cv2
import mediapipe as mp
import pandas as pd

from backend.app.config.path_settings import APP_TEMPLATES_PATH

mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_holistic = mp.solutions.holistic


def create_frame_landmark_df(results, frame):
    xyz = pd.read_parquet(f'{APP_TEMPLATES_PATH}/parquets/10042041.parquet')
    xyz_skew = xyz[["type", "landmark_index"]].drop_duplicates().reset_index(drop=True).copy()

    face = pd.DataFrame()
    pose = pd.DataFrame()
    left_hand = pd.DataFrame()
    right_hand = pd.DataFrame()

    if results.face_landmarks:
        for i, point in enumerate(results.face_landmarks.landmark):
            face.loc[i, ["x", "y", "z"]] = [point.x, point.y, point.z]

    if results.pose_landmarks:
        for i, point in enumerate(results.pose_landmarks.landmark):
            pose.loc[i, ["x", "y", "z"]] = [point.x, point.y, point.z]

    if results.left_hand_landmarks:
        for i, point in enumerate(results.left_hand_landmarks.landmark):
            left_hand.loc[i, ["x", "y", "z"]] = [point.x, point.y, point.z]

    if results.right_hand_landmarks:
        for i, point in enumerate(results.right_hand_landmarks.landmark):
            right_hand.loc[i, ["x", "y", "z"]] = [point.x, point.y, point.z]

    face = (
        face.reset_index()
        .rename(columns={"index": "landmark_index"})
        .assign(type="face")
    )

    pose = (
        pose.reset_index()
        .rename(columns={"index": "landmark_index"})
        .assign(type="pose")
    )

    left_hand = (
        left_hand.reset_index()
        .rename(columns={"index": "landmark_index"})
        .assign(type="left_hand")
    )

    right_hand = (
        right_hand.reset_index()
        .rename(columns={"index": "landmark_index"})
        .assign(type="right_hand")
    )

    landmarks = pd.concat([face, pose, left_hand, right_hand]).reset_index(drop=True)
    landmarks = xyz_skew.merge(landmarks, on=["type", "landmark_index"], how="left")
    return landmarks.assign(frame=frame)


def do_capture_loop(video_path):
    if video_path is None:
        video_path = 0

    all_landmarks = []
    try:
        cap = cv2.VideoCapture(video_path)
        with mp_holistic.Holistic(
                min_detection_confidence=0.5, min_tracking_confidence=0.5) as holistic:

            frame = 0
            while cap.isOpened():
                frame += 1
                success, image = cap.read()
                if not success:
                    print("Not found frame.")
                    break

                image.flags.writeable = False
                image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
                results = holistic.process(image)
                landmarks = create_frame_landmark_df(results, frame)
                all_landmarks.append(landmarks)
                # image.flags.writeable = True
                # image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
                # mp_drawing.draw_landmarks(
                #     image,
                #     results.face_landmarks,
                #     mp_holistic.FACEMESH_CONTOURS,
                #     landmark_drawing_spec=None,
                #     connection_drawing_spec=mp_drawing_styles
                #     .get_default_face_mesh_contours_style()
                # )
                # mp_drawing.draw_landmarks(
                #     image,
                #     results.pose_landmarks,
                #     mp_holistic.POSE_CONNECTIONS,
                #     landmark_drawing_spec=mp_drawing_styles
                #     .get_default_pose_landmarks_style()
                # )
                # cv2.imshow('Holistic', cv2.flip(image, 1))
                # if cv2.waitKey(5) & 0xFF == ord('q'):
                #     break
    except Exception as e:
        logging.log(logging.ERROR, e)
        return landmarks
    finally:
        cap.release()
        cv2.destroyAllWindows()

    return all_landmarks
