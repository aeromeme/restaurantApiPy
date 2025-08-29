from models.models import OrderDetails

def sync_order_domain_to_orm(domain_order, orm_order, session):
    orm_order.CustomerName = domain_order.customer_name
    orm_order.OrderDate = domain_order.order_date

    # Sync OrderDetails (remove, update, add)
    existing_details = {d.OrderDetailID: d for d in orm_order.OrderDetails}
    updated_details = {d.order_detail_id: d for d in domain_order.order_details if hasattr(d, 'order_detail_id')}

    # Remove details not in updated_order
    for detail_id in list(existing_details):
        if detail_id not in updated_details:
            session.delete(existing_details[detail_id])

    # Add or update details
    for upd_detail in domain_order.order_details:
        if hasattr(upd_detail, 'order_detail_id') and upd_detail.order_detail_id in existing_details:
            # Update existing
            db_detail = existing_details[upd_detail.order_detail_id]
            db_detail.ProductID = upd_detail.product_id
            db_detail.Quantity = upd_detail.quantity
            db_detail.Price = upd_detail.price
        else:
            # New detail
            new_detail = OrderDetails(
                ProductID=upd_detail.product_id,
                Quantity=upd_detail.quantity,
                Price=upd_detail.price
            )
            orm_order.OrderDetails.append(new_detail)
