from sqlalchemy.orm import Session
from typing import Type, List, Dict, Optional
from Repositories.database import Base


class CRUD:
    def __init__(self, model: Type[Base], session: Session):
        self.model = model
        self.session = session

    def get(self, record_id: int) -> Optional[Base]:
        """ Получить запись по ID """
        return self.session.query(self.model).filter(self.model.id == record_id).first()

    def get_all(self, filters: Optional[Dict[str, any]] = None, limit: Optional[int] = None,
                page: Optional[int] = 1) -> List[Type[Base]]:
        """ Получить все записи с возможностью фильтрации по полям, пагинации и автоматическим расчётом offset """
        query = self.session.query(self.model)

        # Применение фильтров
        if filters:
            for field, value in filters.items():
                column = getattr(self.model, field, None)
                if column:
                    query = query.filter(column == value)

        # Применение лимита
        if limit is not None:
            query = query.limit(limit)

        # Вычисление offset, если передан page
        if page is not None:
            offset = (page - 1) * limit if limit is not None else 0
            query = query.offset(offset)

        return query.all()

    def create(self, data: Dict[str, any]) -> Base:
        """ Создать новую запись """
        instance = self.model(**data)
        self.session.add(instance)
        self.session.commit()
        return instance

    def update(self, record_id: int, data: Dict[str, any]) -> Optional[Base]:
        """ Обновить запись по ID """
        instance = self.get_by_id(record_id)
        if instance:
            for key, value in data.items():
                setattr(instance, key, value)
            self.session.commit()
            return instance
        return None

    def delete(self, record_id: int) -> bool:
        """ Удалить запись по ID """
        instance = self.get_by_id(record_id)
        if instance:
            self.session.delete(instance)
            self.session.commit()
            return True
        return False
