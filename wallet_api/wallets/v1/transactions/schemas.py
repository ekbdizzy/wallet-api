from drf_yasg import openapi

# More about scheme is here:
# rest_framework_json_api.schemas.openapi.AutoSchema 

TRANSACTIONS_CREATE_BODY_SCHEMA = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        "data": openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "type": openapi.Schema(
                    type=openapi.TYPE_STRING,
                    default='TransactionListCreateView'
                ),
                "attributes": openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        "wallet_id": openapi.Schema(type=openapi.TYPE_INTEGER),
                        "amount": openapi.Schema(type=openapi.TYPE_STRING),
                        "is_inbound": openapi.Schema(type=openapi.TYPE_BOOLEAN),
                    }
                )
            }
        )
    },
)