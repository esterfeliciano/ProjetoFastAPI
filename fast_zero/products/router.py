from fast_zero.config.database_settings import get_session
from sqlalchemy import select
from sqlalchemy.orm import Session

from fast_zero.products.models import Product
from fast_zero.products.schemas import (
    ProductList,
    ProductPublic,
    ProductSchema,
    ProductUpdate,
)
from fast_zero.users.models import User
from fast_zero.users.security import get_current_user

router = APIRouter(prefix='/products', tags=['products'])


@router.post(
    '/',
    status_code=status.HTTP_201_CREATED,
    response_model=ProductPublic,
)
def create_product(
    product: ProductSchema,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    db_product = session.scalar(
        select(Product).where(Product.name == product.name)
    )
    if db_product:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Product already exists',
        )

    db_product = Product(
        name=product.name,
        description=product.description,
        price=product.price,
        stock=product.stock,
        category=product.category,
    )
    session.add(db_product)
    session.commit()
    session.refresh(db_product)

    return db_product


@router.get('/', response_model=ProductList)
def read_products(
    skip: int = 0,
    limit: int = 100,
    session: Session = Depends(get_session),
):
    products = session.scalars(select(Product).offset(skip).limit(limit)).all()
    return {'products': products}


@router.get('/{product_id}', response_model=ProductPublic)
def read_product(
    product_id: int,
    session: Session = Depends(get_session),
):
    db_product = session.scalar(
        select(Product).where(Product.id == product_id)
    )
    if not db_product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Product not found',
        )
    return db_product


@router.put('/{product_id}', response_model=ProductPublic)
def update_product(
    product_id: int,
    product: ProductUpdate,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    db_product = session.scalar(
        select(Product).where(Product.id == product_id)
    )
    if not db_product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Product not found',
        )

    for key, value in product.model_dump(exclude_unset=True).items():
        setattr(db_product, key, value)

    session.commit()
    session.refresh(db_product)
    return db_product


@router.delete('/{product_id}', status_code=status.HTTP_200_OK)
def delete_product(
    product_id: int,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    db_product = session.scalar(
        select(Product).where(Product.id == product_id)
    )
    if not db_product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Product not found',
        )

    session.delete(db_product)
    session.commit()

    return {'message': 'Product deleted successfully'}
