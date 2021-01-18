let cells = document.getElementsByClassName('schedule-cell')
let start_input = document.getElementById('id_start')
let end_input = document.getElementById('id_end')
let current_date = document.getElementById('current_date')

for (let i = 0; i < cells.length; i++) {
    cells[i].addEventListener('mousedown', mouseDownCell)
    cells[i].addEventListener('mouseup', mouseUpCell)
    cells[i].addEventListener('mouseenter', mouseEnterCell)
    cells[i].addEventListener('mouseleave', mouseLeaveCell)

}

function mouseDownCell(e) {
    e.target.style.backgroundColor = '0052AA'
    e.target.style.color = 'ffffff'
}

function fixDigit(val) {
    return val.toString().length === 1 ? "0" + val : val;
}

function mouseUpCell(e) {
    e.target.style.backgroundColor = '007BFF'
    e.target.style.color = 'ffffff'
    let y_m_d = current_date.innerText
    let h_m = e.target.innerText
    let dateString = y_m_d + 'T' + h_m
    start_input.value = dateString

    let interval = parseInt(document.getElementById('interval').innerText)
    let start_date = new Date(dateString)
    let end_date = start_date
    end_date.setMinutes(start_date.getMinutes() + interval)
    let y = end_date.getFullYear()
    let mo = fixDigit(end_date.getMonth() + 1)
    let d = fixDigit(end_date.getDate())
    y_m_d = y + '-' + mo + '-' + d
    let h = fixDigit(end_date.getHours())
    let mi = fixDigit(end_date.getMinutes())
    h_m = h + ':' + mi
    let endDateString = y_m_d + 'T' + h_m
    end_input.value = endDateString
}

function mouseEnterCell(e) {
    e.target.style.backgroundColor = '007BFF'
    e.target.style.color = 'ffffff'
}

function mouseLeaveCell(e) {
    e.target.style.backgroundColor = 'ffffff'
    e.target.style.color = '212529'
}

