import React from "react";

const ScheduleResultTable = ({ schedule, selectedDoctorCode, firstDay }) => {
  console.log("firstDay:", firstDay);

  // schedule yoksa veya boşsa tabloyu hiç göstermeyelim, sadece null dönderelim.
  if (!schedule || schedule.length === 0) {
    return null;
  }

  const daysOfWeek = ["Pazartesi", "Salı", "Çarşamba", "Perşembe", "Cuma", "Cumartesi", "Pazar"];

  // firstDay string olarak geliyor, bunu dizideki index değerine çevirelim.
  let firstDayIndex = daysOfWeek.indexOf(firstDay);

  // Eğer firstDayIndex -1 dönerse (geçersiz değer), varsayılan olarak 0 (Pazartesi) seç
  if (firstDayIndex === -1) {
    console.error(`Geçersiz gün adı: ${firstDay}, varsayılan olarak "Pazartesi" alındı.`);
    firstDayIndex = 0;
  }

  const totalDays = schedule.length; // Ay içindeki toplam gün sayısı
  const weeks = [];
  let dayCounter = 1;

  // İlk haftayı oluştururken firstDayIndex kadar boşluk ekleyelim
  let firstWeek = new Array(firstDayIndex).fill(null); // İlk gün öncesini boş yap
  for (let i = firstDayIndex; i < 7; i++) {
    if (dayCounter <= totalDays) {
      firstWeek.push(schedule[dayCounter - 1]);
      dayCounter++;
    } else {
      firstWeek.push(null);
    }
  }
  weeks.push(firstWeek);

  // Sonraki haftaları 7'şer 7'şer dolduralım
  while (dayCounter <= totalDays) {
    let week = [];
    for (let i = 0; i < 7; i++) {
      if (dayCounter <= totalDays) {
        week.push(schedule[dayCounter - 1]);
        dayCounter++;
      } else {
        week.push(null);
      }
    }
    weeks.push(week);
  }

  return (
    <div className="table-responsive mt-4">
      <table className="table table-dark table-bordered shadow-md text-center rounded-3" style={{ minWidth: "800px" }}>
        <thead>
          <tr>
            {daysOfWeek.map((day, index) => (
              <th key={index} className="text-center">
                {day}
              </th>
            ))}
          </tr>
        </thead>
        <tbody>
          {weeks.map((week, weekIndex) => (
            <tr key={weekIndex}>
              {week.map((shift, dayIndex) => (
                <td key={dayIndex}>
                  {shift ? (
                    <>
                      <strong className="d-flex justify-content-center bg-warning text-dark mb-1">
                        {weekIndex * 7 + dayIndex - firstDayIndex + 1}. Gün
                      </strong>
                      {shift[0].map((code, index) => (
                        <span key={index} className={code === selectedDoctorCode ? "selected-doctor" : ""}>
                          {code}{" "}
                        </span>
                      ))}
                      <br />
                      {shift[1].map((code, index) => (
                        <span key={index} className={code === selectedDoctorCode ? "selected-doctor" : ""}>
                          {code}{" "}
                        </span>
                      ))}
                    </>
                  ) : null}
                </td>
              ))}
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};

export default ScheduleResultTable;
