import json
from odoo import http
from odoo.http import request


class PropertyApi(http.Controller):
    @http.route("/v1/property", methods=["POST"], type="http", auth="none", csrf=False)
    def post_property(self):
        args = request.httprequest.data.decode()
        vals = json.loads(args)
        # separate method
        if not vals.get("name"):
            return request.make_json_response({
                "error": "Field name is required",
            }, status=400)
        try:
            res = request.env['property'].sudo().create(vals)
            if res:
                return request.make_json_response({
                    "message": f"{res.name} has been created successfully",
                    "id": res.id,
                    "name": res.name,
                }, status=201)
        except Exception as error:
            return request.make_json_response({
                "error": error,
            }, status=400)

    @http.route("/v1/property/<int:id>", methods=["PUT"], type="http", auth="none", csrf=False)
    def update_property(self, id):
        try:
            property_id = request.env['property'].sudo().search([('id', '=', id)])
            if not property_id:
                return request.make_json_response({
                    "error": f"There is no property with id: {id} !!!",
                }, status=400)
            args = request.httprequest.data.decode()
            vals = json.loads(args)
            property_id.write(vals)
            return request.make_json_response({
                "message": f"{property_id.name} has been updated successfully",
                "id": property_id.id,
                "name": property_id.name,
            }, status=200)
        except Exception as error:
            return request.make_json_response({
                "error": error,
            }, status=400)

    @http.route("/v1/property/<int:id>", methods=["GET"], type="http", auth="none", csrf=False)
    def get_property(self, id):
        try:
            property_id = request.env['property'].sudo().search([('id', '=', id)])
            if not property_id:
                return request.make_json_response({
                    "error": f"There is no property with id: {id} !!!",
                }, status=400)
            return request.make_json_response({
                "name": property_id.name,
                "postcode": property_id.postcode,
                "bedrooms": property_id.bedrooms,
                "living_area": property_id.living_area,
                "description": property_id.description,
                "garden": property_id.garden,
                "garden_area": property_id.garden_area,
                "garden_orientation": property_id.garden_orientation,
            }, status=200)
        except Exception as error:
            return request.make_json_response({
                "error": error,
            }, status=400)

    # @http.route("/v1/property/json", methods=["POST"], type="json", auth="none", csrf=False)
    # def post_property_json(self):
    #     args = request.httprequest.data.decode()
    #     vals = json.loads(args)
    #     print(vals)
    #     res = request.env['property'].sudo().create(vals)
    #     if res:
    #         return {
    #             "message": f"{vals["name"]} has been created successfully"
    #         }
