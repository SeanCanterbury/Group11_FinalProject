from . import orders, order_details, ratings, resources, promos, sandwiches



def load_routes(app):
    app.include_router(orders.router)
    app.include_router(order_details.router)
    #print("next is ratings")
    app.include_router(ratings.router)
    app.include_router(resources.router)
    app.include_router(promos.router)
    app.include_router(sandwiches.router)
