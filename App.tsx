import { useEffect, useState } from 'react';
import axios from 'axios';
import { format, addDays } from 'date-fns'; // Для удобной работы с датой
import ruLocale from 'date-fns/locale/ru'; // Локализация даты
import './styles.css'; // Ваш файл стилей Tailwind

// Интерфейсы данных
interface IRoom {
  id: number;
  name: string;
}

interface IBooking {
  id: number;
  room_id: number;
  start_time: string; // ISO DateTime
  end_time: string;
  status: string;
}

const BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

export default function BookingPage() {
  const [rooms, setRooms] = useState<IRoom[]>([]);
  const [selectedDate, setSelectedDate] = useState<Date>(new Date());
  const [bookings, setBookings] = useState<IBooking[]>([]);

  // Загрузка списка комнат при монтировании компонента
  useEffect(() => {
    async function fetchRooms() {
      try {
        const res = await axios.get(`${BASE_URL}/api/v1/rooms`);
        setRooms(res.data);
      } catch (error) {
        console.error('Ошибка загрузки комнат:', error);
      }
    }
    fetchRooms();
  }, []);

  // Загрузка расписания при изменении даты
  useEffect(() => {
    if (!rooms.length) return;

    async function fetchBookings() {
      try {
        const dateStr = format(selectedDate, 'yyyy-MM-dd');
        const promises = rooms.map(async (room) => {
          const res = await axios.get(
            `${BASE_URL}/api/v1/bookings/room/${room.id}?date=${dateStr}`
          );
          return { roomId: room.id, bookings: res.data };
        });

        const results = await Promise.all(promises);
        const bookingMap = Object.fromEntries(results.map(r => [r.roomId, r.bookings]));
        
        // Преобразуем данные для отображения
        const dataForUI = rooms.map((room) => ({
          ...room,
          bookings: bookingMap[room.id].map(b => ({
            start: b.start_time.split('T')[1], // Только время
            end: b.end_time.split('T')[1],
            status: b.status,
          }))
        }));

        setBookings(dataForUI);
      } catch (error) {
        console.error('Ошибка загрузки бронирований:', error);
      }
    }
    fetchBookings();
  }, [selectedDate]);

  // Компонент календаря (упрощённая версия)
  const Calendar = () => (
    <div>
      <button onClick={() => setSelectedDate(addDays(selectedDate, -7))}>←</button>
      <span>{format(selectedDate, 'dd MMMM yyyy', { locale: ruLocale })}</span>
      <button onClick={() => setSelectedDate(addDays(selectedDate, 7))}>→</button>
    </div>
  );

  // Основной рендеринг
  return (
    <main className="p-4">
      {/* Календарь */}
      <Calendar />

      {/* Список комнат с расписанием */}
      <ul className="grid grid-cols-1 md:grid-cols-3 gap-6 mt-6">
        {bookings.map((room) => (
          <li key={room.id} className="bg-white shadow-md rounded-lg overflow-hidden">
            <header className="px-4 py-3 border-b border-gray-200 flex justify-between items-center">
              <h3 className="text-lg font-medium">{room.name}</h3>
              <span className={`inline-block px-2 py-1 text-xs ${room.bookings.some(b => b.status === 'active') ? 'bg-red-500' : 'bg-green-500'} text-white rounded-full`}>
                {room.bookings.some(b => b.status === 'active') ? 'Занято' : 'Свободно'}
              </span>
            </header>
            <table className="w-full divide-y divide-gray-200">
              <thead>
                <tr>
                  <th className="py-2 pl-4 pr-3 text-left">Время начала</th>
                  <th className="py-2 pl-4 pr-3 text-left">Время окончания</th>
                  <th className="py-2 pl-4 pr-3 text-left">Статус</th>
                </tr>
              </thead>
              <tbody>
                {room.bookings.length > 0 ? (
                  room.bookings.map((b, i) => (
                    <tr key={i} className={`${i % 2 !== 0 && 'bg-gray-50'}`}>
                      <td className="py-2 pl-4 pr-3 whitespace-nowrap">{b.start}</td>
                      <td className="py-2 pl-4 pr-3 whitespace-nowrap">{b.end}</td>
                      <td className="py-2 pl-4 pr-3 whitespace-nowrap" style={{ color: b.status === 'active' ? '#e53e3e' : '#48bb78' }}>
                        {b.status.charAt(0).toUpperCase() + b.status.slice(1)}
                      </td>
                    </tr>
                  ))
                ) : (
                  <tr><td colSpan={3} className="py-4 text-center italic">Нет забронированных слотов.</td></tr>
                )}
              </tbody>
            </table>
          </li>
        ))}
      </ul>
    </main>
  );
}
