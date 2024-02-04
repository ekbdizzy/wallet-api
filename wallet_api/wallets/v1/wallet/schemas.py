from drf_yasg import openapi

# More about scheme is here:
# rest_framework_json_api.schemas.openapi.AutoSchema 

WALLET_CREATE_BODY_SCHEMA = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        "data": openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "type": openapi.Schema(
                    type=openapi.TYPE_STRING,
                    default='WalletListCreateView'
                ),
                "attributes": openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        "label": openapi.Schema(type=openapi.TYPE_STRING)
                    }
                )
            }
        )
    },
)

WALLET_DETAIL_BODY_SCHEMA = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        "data": openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "type": openapi.Schema(
                    type=openapi.TYPE_STRING,
                    default='WalletDetailView'
                ),
                "id": openapi.Schema(
                    type=openapi.TYPE_INTEGER,
                ),
                "attributes": openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        "label": openapi.Schema(type=openapi.TYPE_STRING)
                    }
                )
            }
        )
    },
)
