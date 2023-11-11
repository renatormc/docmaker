from typing import Optional
# from doctpl.custom_types import  ModelInfo
from doctpl.gui.widgets.scomposite import SComposite
from doctpl.gui.widgets.widget import WidgetMatrix
from PySide6.QtWidgets import QFileDialog
import json
from pathlib import Path
# from database import repo


class BaseForm(SComposite):
    widgets: WidgetMatrix = []
    name = "No name"
    templates_dir = ""

    def __init__(self):
        super(BaseForm, self).__init__(self.widgets, model_name=self.name)
        
    

    # def save_last_data(self):
    #     data = self.serialize()
    #     repo.save_last_data(self.model_info.name,  data)

    # def load_last_data(self):
    #     data = repo.get_last_data(self.model_info.name)
    #     self.load(data)

    def save_to_file(self, file_: Optional[str] = None):
        data = self.serialize()
        file_= file_ or QFileDialog.getSaveFileName(self, "Escolha o arquivo",  ".", "JSON (*.json)")[0]
        if file_:
            with Path(file_).open("w", encoding="utf-8") as f:
                f.write(json.dumps(data, ensure_ascii=False, indent=4))


    def load_from_file(self, file_: Optional[str] = None) -> None:
        file_ = file_ or QFileDialog.getOpenFileName(self, "Escolha o arquivo",  ".", "JSON (*.json)")[0]
        if file_:
            path = Path(file_)
            if path.exists():
                with Path(file_).open("r", encoding="utf-8") as f:
                    data = json.load(f)
                self.load(data)

    def pre_process(self, context: dict) -> dict:
        return context
    

    # def load_data(self, data: dict) -> None:
    #     for key, w in self.widgets_map.items():
    #         try:
    #             w.load(data[key])
    #         except Exception:
    #             pass

    # def clear_content(self):
    #     for row in self.widgets:
    #         for item in row:
    #             item.clear_content()
