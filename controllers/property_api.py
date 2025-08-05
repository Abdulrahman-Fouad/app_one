import json

from odoo import http
from odoo.http import request

class PropertyApi(http.Controller):
    @http.route("/v1/property", methods=["POST"], type="http", auth="none", csrf= False)
    def post_property(self):
        args = request.httprequest.data.decode()
        vals = json.loads(args)
        # separate method
        if not vals.get("name"):
            return request.make_json_response({
                "message": "Field name is required",
            }, status=400)
        try:
            res = request.env['property'].sudo().create(vals)
            if res:
                return request.make_json_response({
                    "message": f"{res.name} has been created successfully",
                    "id": res.id,
                    "name": res.name,
                }, status = 201)
        except Exception as error:
            return request.make_json_response({
                "message": error,
            }, status=400)


    @http.route("/v1/property/json", methods=["POST"], type="json", auth="none", csrf=False)
    def post_property_json(self):
        args = request.httprequest.data.decode()
        vals = json.loads(args)
        print(vals)
        res = request.env['property'].sudo().create(vals)
        if res:
            return {
                "message": f"{vals["name"]} has been created successfully"
            }

