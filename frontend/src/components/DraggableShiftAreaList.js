import React, { useEffect, useState } from "react";
import { DragDropContext, Droppable, Draggable } from "@hello-pangea/dnd";
import "bootstrap/dist/css/bootstrap.min.css";

export default function DraggableShiftAreaList({ allShiftAreas, activeAreaNames, onUpdate }) {
  const [items, setItems] = useState([]);

  useEffect(() => {
    const mappedActive = activeAreaNames
      .map((areaName) => {
        const found = allShiftAreas.find((a) => a.area_name === areaName);
        if (!found) return null;
        return { id: found.id.toString(), name: found.area_name, active: true };
      })
      .filter(Boolean);

    const mappedPassive = allShiftAreas
      .filter((a) => !activeAreaNames.includes(a.area_name))
      .map((a) => ({ id: a.id.toString(), name: a.area_name, active: false }));

    setItems([...mappedActive, ...mappedPassive]);
  }, [allShiftAreas, activeAreaNames]);

  const handleDragEnd = (result) => {
    if (!result.destination) return;

    const newList = Array.from(items);
    const [movedItem] = newList.splice(result.source.index, 1);
    newList.splice(result.destination.index, 0, movedItem);

    setItems(newList);
    const onlyActive = newList.filter((it) => it.active).map((it) => it.name);
    onUpdate?.(onlyActive);
  };

  const toggleActive = (id) => {
    setItems((prev) => {
      const updated = prev.map((x) => (x.id === id ? { ...x, active: !x.active } : x));
      const onlyActive = updated.filter((it) => it.active).map((it) => it.name);
      onUpdate?.(onlyActive);
      return updated;
    });
  };

  return (
    <div className="container">
      <DragDropContext onDragEnd={handleDragEnd}>
        <Droppable droppableId="shiftList">
          {(provided) => (
            <ul ref={provided.innerRef} {...provided.droppableProps} className="list-group">
              {items.map((item, index) => (
                <Draggable key={item.id} draggableId={item.id} index={index} isDragDisabled={!item.active}>
                  {(provided, snapshot) => (
                    <li
                      ref={provided.innerRef}
                      {...provided.draggableProps}
                      {...provided.dragHandleProps}
                      onClick={() => toggleActive(item.id)}
                      className={`list-group-item d-flex justify-content-between align-items-center shadow-sm ${
                        item.active ? "bg-white text-dark" : "bg-light text-secondary"
                      }`}
                      style={{
                        cursor: item.active ? "grab" : "pointer",
                        marginBottom: "8px",
                        border: "1px solid #ddd",
                        borderRadius: "6px",
                        transition: "background 0.3s ease",
                        ...provided.draggableProps.style,
                      }}
                    >
                      {item.name}
                      <span className={`badge ${item.active ? "bg-success" : "bg-danger"}`}>{item.active ? "Aktif" : "Pasif"}</span>
                    </li>
                  )}
                </Draggable>
              ))}
              {provided.placeholder}
            </ul>
          )}
        </Droppable>
      </DragDropContext>
    </div>
  );
}
