from ultralytics import YOLO
from ultralytics.engine.results import Results
import cv2
import json
import os.path
import shutil


def process_img(file_dir: str, filename: str) -> bool:
    """Детекция судов на фото и сохранение результатов"""
    try:
        model = YOLO('yolov8n.pt')
        results: list[Results] = model(os.path.join(file_dir, filename))
        boats = [box.cls for box in results[0].boxes if box.cls == 8]

        # Формирование фото с результатами
        res_name = "result_"+filename
        res_path = os.path.join(file_dir, res_name)
        res_img = results[0].plot()
        cv2.imwrite(res_path, res_img)

        # Формирование JSON с колв-ом кораблей
        json_name = "data.json"
        json_data = {'count': len(boats)}
        json_path = os.path.join(file_dir, json_name)
        with open(json_path, 'w') as json_f:
            json.dump(json_data, json_f)

        return True

    except Exception as ex:
        print(ex)
        shutil.rmtree(file_dir)
        return False


    # for box in results[0].boxes:
    #     # print(type(box))
    #     box: Boxes
    #     cls = int(box.cls)
    #     conf = float(box.conf)
    #     print(model.names[cls], cls,conf, box.xywh[0].tolist())
