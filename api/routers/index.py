from . import orders, order_details, ratings, resources



def load_routes(app):
    app.include_router(orders.router)
    app.include_router(order_details.router)
    #print("next is ratings")
    app.include_router(ratings.router)
    app.include_router(resources.router)
