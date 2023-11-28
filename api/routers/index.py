from . import orders, order_details, ratings



def load_routes(app):
    app.include_router(orders.router)
    app.include_router(order_details.router)
    #print("next is ratings")
    app.include_router(ratings.router)
