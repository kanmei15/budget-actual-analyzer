let currentGroupedData = null;

// イベントリスナーと初期表示処理
document.addEventListener('DOMContentLoaded', () => {
    document.getElementById('source-select').addEventListener('change', async function () {
        const sourceType = this.value;
        const apiUrl = getApiUrl(sourceType);
        const map = getFieldMap(sourceType);
        const data = await fetchData(apiUrl, 5, 200);
        currentGroupedData = groupDataByParent(data, map);
        renderTable(currentGroupedData);
    });

    document.getElementById('period-select').addEventListener('change', function () {
        if (currentGroupedData) {
            renderTable(currentGroupedData);
        }
    });

    // 初期表示トリガー
    document.getElementById('source-select').dispatchEvent(new Event('change'));
});

// --- Utility functions ---

// APIエンドポイントを sourceType に応じて返す
function getApiUrl(sourceType) {
    return sourceType === '2' ? '/api/difference' : `/api/aggregated?source_type=${sourceType}`;
}

// sourceType に応じたフィールド名のマッピングを返す
function getFieldMap(sourceType) {
    const fieldMap = {
        '0': {
            internal: 'total_internal_man_hours',
            partner: 'total_partner_man_hours',
            bulk: 'total_bulk_man_hours',
            order: 'total_order_amount',
            sales: 'total_sales',
            profit: 'total_profit'
        },
        '1': {
            internal: 'total_internal_man_hours',
            partner: 'total_partner_man_hours',
            bulk: 'total_bulk_man_hours',
            order: 'total_order_amount',
            sales: 'total_sales',
            profit: 'total_profit'
        },
        '2': {
            internal: 'diff_internal_man_hours',
            partner: 'diff_partner_man_hours',
            bulk: 'diff_bulk_man_hours',
            order: 'diff_order_amount',
            sales: 'diff_sales',
            profit: 'diff_profit'
        }
    };
    return fieldMap[sourceType];
}

// 指定URLからデータを取得し、JSONとして返す
async function fetchData(apiUrl, retries = 5, delay = 200) {
    //const response = await fetch(apiUrl, {
    //    method: 'GET',
    //    headers: {
    //        "Content-Type": "application/json"
    //    }
    //});
    //return await response.json();
    for (let attempt = 1; attempt <= retries; attempt++) {
        try {
            const response = await fetch(apiUrl, {
                method: 'GET',
                headers: {
                    "Content-Type": "application/json"
                }
            });

            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }

            return await response.json();

        } catch (error) {
            console.warn(`Fetch failed (attempt ${attempt}/${retries}):`, error);

            if (attempt < retries) {
                await new Promise(res => setTimeout(res, delay * Math.pow(3, attempt - 1)));
            } else {
                throw new Error(`API fetch failed after ${retries} attempts`);
            }
        }
    }
}

// データを親キー、グループキー、月で分類してネスト構造に変換
function groupDataByParent(data, map) {
    const parentGrouped = {};
    data.forEach(row => {
        const parentKey = row.parent_group_key ?? '未分類';
        const groupKey = row.group_by_key;
        const month = row.month_number;

        if (!parentGrouped[parentKey]) parentGrouped[parentKey] = {};
        if (!parentGrouped[parentKey][groupKey]) parentGrouped[parentKey][groupKey] = {};

        parentGrouped[parentKey][groupKey][month] = extractMappedValues(row, map);
    });
    return parentGrouped;
}

// 指定されたマッピングに従って、必要な値を抽出
function extractMappedValues(row, map) {
    return {
        internal: row[map.internal],
        partner: row[map.partner],
        bulk: row[map.bulk],
        order: row[map.order],
        sales: row[map.sales],
        profit: row[map.profit],
    };
}

// グループ化されたデータをもとにテーブルを描画
function renderTable(groupedData) {
    const period = document.getElementById('period-select')?.value || 'all';
    renderHeader(period); // テーブルヘッダ描画

    const tbody = document.querySelector('#results-table tbody');
    tbody.innerHTML = '';

    const grandTotal = defaultValue(); // 全体合計初期化

    for (const [parentKey, groupData] of Object.entries(groupedData)) {
        appendHeaderRow(tbody, parentKey); // 親グループ見出し追加
        const groupSum = {};

        for (const [groupKey, months] of Object.entries(groupData)) {
            const tr = createRow(groupKey, months, groupSum, false, period);
            tbody.appendChild(tr);
        }

        // グループ内合計行
        const totalRow = createRow('グループ合計', groupSum, {}, true, period);
        tbody.appendChild(totalRow);

        // グループ合計を全体合計に加算
        for (const month in groupSum) {
            if (!grandTotal[month]) grandTotal[month] = defaultValue();
            for (const key in groupSum[month]) {
                grandTotal[month][key] += groupSum[month][key];
            }
        }
    }

    // 全体合計行（部門合計）を追加
    const grandTotalRow = createRow('部門合計', grandTotal, {}, true, period);
    tbody.appendChild(grandTotalRow);
}

// 親グループ名の行をテーブルに追加
function appendHeaderRow(tbody, parentKey) {
    const headerRow = document.createElement('tr');
    headerRow.innerHTML = `<td colspan="106" class="parent-header">${parentKey}</td>`;
    tbody.appendChild(headerRow);
}

// 単一のデータ行（または合計行）を作成
function createRow(label, months, accumulator = {}, isSummary = false, period = 'all') {
    const tr = document.createElement('tr');
    tr.innerHTML = `<td class="${isSummary ? 'summary-cell' : ''} group-key">${label}</td>`;

    const halfYearTotals = defaultValue();
    const secondHalfTotals = defaultValue();
    const fullYearTotals = defaultValue();

    for (let m = 2; m <= 13; m++) {
        const month = m <= 12 ? m : 1;
        const val = months[month] || defaultValue();

        if (accumulator && !accumulator[month]) accumulator[month] = defaultValue();
        if (accumulator) {
            for (let key in val) accumulator[month][key] += val[key] ?? 0;
        }

        if (m >= 2 && m <= 7) addToTotal(halfYearTotals, val);
        if (m >= 8 && m <= 13) addToTotal(secondHalfTotals, val);
        addToTotal(fullYearTotals, val);

        if (period === 'all' || period === `month_${month}`) {
            tr.innerHTML += generateDataCells(val, isSummary);
        }
    }

    if (period === 'first_half') {
        tr.innerHTML += generateDataCells(halfYearTotals, isSummary);
    } else if (period === 'second_half') {
        tr.innerHTML += generateDataCells(secondHalfTotals, isSummary);
    } else if (period === 'full_year') {
        tr.innerHTML += generateDataCells(fullYearTotals, isSummary);
    } else if (period === 'all') {
        tr.innerHTML += `
            ${generateDataCells(halfYearTotals, isSummary)}
            ${generateDataCells(secondHalfTotals, isSummary)}
            ${generateDataCells(fullYearTotals, isSummary)}
        `;
    }

    return tr;
}

// 合計値に指定値を加算
function addToTotal(target, source) {
    for (const key in target) {
        target[key] += source[key] ?? 0;
    }
}

// セルデータをHTMLに変換（工数、金額、利益率など）
function generateDataCells(val, isSummary) {
    const rateValue = val.sales ? (val.profit / val.sales) * 100 : null;
    const rateText = rateValue !== null
        ? (Math.abs(rateValue) > 100 ? '±Over' : rateValue.toFixed(2) + '%')
        : '-';

    const getClass = (v, type) => {
        const negative = typeof v === 'number' && v < 0 ? 'negative' : '';
        return `${negative} ${isSummary ? 'summary-cell' : ''} ${type}`;
    };

    const base = (v, type) =>
        `<td class="${getClass(v, type)}">${(typeof v === 'number') ? v.toFixed(2) : '0'}</td>`;

    const money = (v, type) =>
        `<td class="${getClass(v, type)}">${(typeof v === 'number') ? Math.round(v / 1000).toLocaleString() : '0'}</td>`;

    return `
        ${base(val.internal, 'internal')}
        ${base(val.partner, 'partner')}
        ${base(val.bulk, 'bulk')}
        ${money(val.order, 'order')}
        ${money(val.sales, 'sales')}
        ${money(val.profit, 'profit')}
        <td class="${getClass(rateValue, 'rate')}">${rateText}</td>
    `;
}

// テーブルヘッダを選択された期間に応じて描画
function renderHeader(period) {
    const thead = document.querySelector('#results-table thead');
    thead.innerHTML = '';

    const tr1 = document.createElement('tr');
    const tr2 = document.createElement('tr');

    tr1.innerHTML = '<th class="group-key" rowspan="2">顧客</th>';

    const labels = ['自社<br />工数', '外注<br />工数', '一括<br />工数', '受注額', '売上計上額', '利益計上額', '利益率'];
    const monthNames = ['2月', '3月', '4月', '5月', '6月', '7月', '8月', '9月', '10月', '11月', '12月', '1月'];

    const addColumnGroup = (label) => {
        tr1.innerHTML += `<th colspan="7">${label}</th>`;
        labels.forEach((_, i) => {
            const classes = ['internal', 'partner', 'bulk', 'order', 'sales', 'profit', 'rate'];
            tr2.innerHTML += `<th class="${classes[i]}">${labels[i]}</th>`;
        });
    };

    if (period === 'all') {
        monthNames.forEach(name => addColumnGroup(name));
        ['上期', '下期', '通期'].forEach(name => addColumnGroup(name));
    } else if (period.startsWith('month_')) {
        const month = parseInt(period.split('_')[1]);
        const index = month === 1 ? 11 : month - 2;
        addColumnGroup(monthNames[index]);
    } else if (period === 'first_half') {
        addColumnGroup('上期');
    } else if (period === 'second_half') {
        addColumnGroup('下期');
    } else if (period === 'full_year') {
        addColumnGroup('通期');
    }

    thead.appendChild(tr1);
    thead.appendChild(tr2);
}

// 各種データ項目の初期値を返す
function defaultValue() {
    return { internal: 0, partner: 0, bulk: 0, order: 0, sales: 0, profit: 0 };
}
