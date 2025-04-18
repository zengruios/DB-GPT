import json
import logging
import xml.etree.ElementTree as ET

from dbgpt.util.json_utils import serialize


class DbDataLoader:
    def get_table_view_by_conn(self, data, speak, sql: str = None):
        param = {}
        api_call_element = ET.Element("chart-view")
        err_msg = None
        try:
            param["type"] = "response_table"
            param["sql"] = sql
            param["data"] = json.loads(
                data.to_json(orient="records", date_format="iso", date_unit="s")
            )
            view_json_str = json.dumps(param, default=serialize, ensure_ascii=False)
        except Exception as e:
            logging.error("parse_view_response error!" + str(e))
            err_param = {}
            err_param["sql"] = f"{sql}"
            err_param["type"] = "response_table"
            err_param["err_msg"] = str(e)
            err_param["data"] = []
            err_msg = str(e)
            view_json_str = json.dumps(err_param, default=serialize, ensure_ascii=False)

        # api_call_element.text = view_json_str
        api_call_element.set("content", view_json_str)
        result = ET.tostring(api_call_element, encoding="utf-8")
        if err_msg:
            return f"""{speak} \\n <span style=\"color:red\">ERROR!</span>{err_msg} 
{result.decode("utf-8")}"""
        else:
            return speak + "\n" + result.decode("utf-8")
