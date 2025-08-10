import json
import math
from urllib.parse import parse_qs

from odoo import http
from odoo.http import request


def valid_response(data, status, pagination_info={}):
    response_body = {"data": data}
    if pagination_info:
        response_body['pagination_info'] = pagination_info

    return request.make_json_response(response_body, status=status)


def invalid_response(error, status):
    response_body = {"error": error}
    return request.make_json_response(response_body, status=status)


class PropertyApi(http.Controller):
    # @http.route("/v1/property", methods=["POST"], type="http", auth="none", csrf=False)
    # def post_property(self):
    #     args = request.httprequest.data.decode()
    #     vals = json.loads(args)
    #     # separate method
    #     if not vals.get("name"):
    #         return invalid_response("Field name is required", 400)
    #     try:
    #         res = request.env['property'].sudo().create(vals)
    #         if res:
    #             return valid_response({
    #                 "message": f"{res.name} has been created successfully",
    #                 "id": res.id,
    #                 "name": res.name,
    #             }, 201)
    #
    #     except Exception as error:
    #         return invalid_response(error, 400)

    @http.route("/v1/property", methods=["POST"], type="http", auth="none", csrf=False)
    def post_property(self):
        args = request.httprequest.data.decode()
        vals = json.loads(args)
        if not vals.get("name"):
            return invalid_response("Field name is required", 400)
        try:
            # res = request.env['property'].sudo().create(vals)
            cr = request.env.cr
            columns = ', '.join(vals.keys())
            values = ', '.join(['%s']* len(vals))
            query = f"""INSERT INTO property ({columns}) VALUES ({values}) RETURNING id, name, postcode, bedrooms"""
            cr.execute(query, tuple(vals.values()))
            res = cr.fetchone()
            print(res)
            if res:
                return valid_response({
                    "message": f"{res[1]} has been created successfully",
                    "id": res[0],
                    "name": res[1],
                }, 201)

        except Exception as error:
            return invalid_response(error, 400)

    @http.route("/v1/property/<int:id>", methods=["PUT"], type="http", auth="none", csrf=False)
    def update_property(self, id):
        try:
            property_id = request.env['property'].sudo().search([('id', '=', id)])
            if not property_id:
                return invalid_response(f"There is no property with id: {id} !!!", 400)
            args = request.httprequest.data.decode()
            vals = json.loads(args)
            property_id.write(vals)
            return valid_response({
                "message": f"{property_id.name} has been updated successfully",
                "id": property_id.id,
                "name": property_id.name,
            }, 200)
        except Exception as error:
            return invalid_response(error, 400)

    @http.route("/v1/property/<int:id>", methods=["GET"], type="http", auth="none", csrf=False)
    def get_property(self, id):
        try:
            property_id = request.env['property'].sudo().search([('id', '=', id)])
            if not property_id:
                return invalid_response(f"There is no property with id: {id} !!!", 400)

            return valid_response({
                "name": property_id.name,
                "postcode": property_id.postcode,
                "bedrooms": property_id.bedrooms,
                "living_area": property_id.living_area,
                "description": property_id.description,
                "garden": property_id.garden,
                "garden_area": property_id.garden_area,
                "garden_orientation": property_id.garden_orientation,
            }, 200)

        except Exception as error:
            return invalid_response(error, 400)

    @http.route("/v1/property/<int:id>", methods=["DELETE"], type="http", auth="none", csrf=False)
    def delete_property(self, id):
        try:
            property_id = request.env['property'].sudo().search([('id', '=', id)])
            if not property_id:
                return invalid_response(f"There is no property with id: {id} !!!", 400)
            property_id.unlink()
            return valid_response({
                "messege": f"Property with id: {id} has been deleted successfully",
            }, 200)
        except Exception as error:
            return invalid_response(error, 400)

    @http.route("/v1/properties", methods=["GET"], type="http", auth="none", csrf=False)
    def get_property_list(self):
        try:
            params = parse_qs(request.httprequest.query_string.decode('utf-8'))
            property_domain = []
            page = offset = None
            limit = 5
            if params:
                if params.get('limit'):
                    limit = int(params.get('limit')[0])
                if params.get('page'):
                    page = int(params.get('page')[0])

            if page:
                offset = (page * limit) - limit

            if params.get('state'):
                property_domain += [('state', '=', params.get('state')[0])]

            property_ids = request.env['property'].sudo().search(property_domain, offset=offset, limit=limit,
                                                                 order='id desc')
            property_count = request.env['property'].sudo().search_count(property_domain)

            if not property_ids:
                return invalid_response("There are no records !!!", 400)
            return valid_response([{
                "id": property_id.id,
                "name": property_id.name,
                "postcode": property_id.postcode,
                "bedrooms": property_id.bedrooms,
                "living_area": property_id.living_area,
                "description": property_id.description,
                "garden": property_id.garden,
                "garden_area": property_id.garden_area,
                "garden_orientation": property_id.garden_orientation,
            } for property_id in property_ids],
                pagination_info={'page': page if page else 1,
                                 'limit': limit,
                                 'pages': math.ceil(property_count / limit) if limit else 1,
                                 'count': property_count
                                 },
                status=200)
        except Exception as error:
            return invalid_response(error, 400)

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
