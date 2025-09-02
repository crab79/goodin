async function loadFinancials() {
    try {
        let response = await fetch("http://140.127.220.85:8000/financials");
        let data = await response.json();

        let tbody = document.getElementById("tagTableBody");
        tbody.innerHTML = ""; // 清空舊資料

        data.forEach(row => {
            let tr = document.createElement("tr");

            // 只取六個欄位
            let fields = ["營收成長率", "稅後淨利率", "ROE(A)－稅後",
                          "自由現金流量(D)", "股利殖利率", "負債比率"];
            fields.forEach(field => {
                let td = document.createElement("td");
                td.textContent = row[field];
                tr.appendChild(td);
            });

            tbody.appendChild(tr);
        });
    } catch (error) {
        console.error("載入財報資料失敗:", error);
    }
}

document.addEventListener("DOMContentLoaded", loadFinancials);
