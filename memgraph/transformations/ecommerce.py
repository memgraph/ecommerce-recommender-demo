import mgp
import json


@mgp.transformation
def rating(messages: mgp.Messages
           ) -> mgp.Record(query=str, parameters=mgp.Nullable[mgp.Map]):
    result_queries = []

    for i in range(messages.total_messages()):
        message = messages.message_at(i)
        rating_dict = json.loads(message.payload().decode('utf8'))
        result_queries.append(
            mgp.Record(
                query=("MERGE (u:User {id: $userId, name: $userName}) "
                       "MERGE (p:Product {id: $productId, name: $productName}) "
                       "CREATE (u)-[:RATED {rating: ToInteger($rating), timestamp: LocalDateTime($timestamp)}]->(p)"),
                parameters={
                    "userId": rating_dict["userId"],
                    "userName": rating_dict["userName"],
                    "productId": rating_dict["productId"],
                    "productName": rating_dict["productName"],
                    "rating": rating_dict["rating"],
                    "timestamp": rating_dict["timestamp"]}))
    return result_queries


@mgp.transformation
def view(messages: mgp.Messages
         ) -> mgp.Record(query=str, parameters=mgp.Nullable[mgp.Map]):
    result_queries = []

    for i in range(messages.total_messages()):
        message = messages.message_at(i)
        view_dict = json.loads(message.payload().decode('utf8'))
        result_queries.append(
            mgp.Record(
                query=("MERGE (u:User {id: $userId, name: $userName}) "
                       "MERGE (p:Product {id: $productId, name: $productName}) "
                       "CREATE (u)-[:VIEWED {timestamp: LocalDateTime($timestamp)}]->(p)"),
                parameters={
                    "userId": view_dict["userId"],
                    "userName": view_dict["userName"],
                    "productId": view_dict["productId"],
                    "productName": view_dict["productName"],
                    "timestamp": view_dict["timestamp"]}))
    return result_queries
