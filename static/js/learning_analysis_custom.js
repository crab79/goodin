/**
 * 學習成效分析頁面 - 自定義 JavaScript
 * 直接操作現有的 HTML 元素，不使用 DataTables 插件
 */

$(document).ready(function() {
    // 模擬學習資料
    const learningData = [
        {
            course: 'A',
            practiceTime: '2024-10-26 10:00',
            errors: 3,
            total: 10,
            accuracy: 70,
            trend: '—',
            errorDetails: [
                { question: 1, userAnswer: 'A', correctAnswer: 'B' },
                { question: 2, userAnswer: 'C', correctAnswer: 'D' },
                { question: 3, userAnswer: 'B', correctAnswer: 'A' }
            ]
        },
        {
            course: 'B',
            practiceTime: '2024-10-25 14:30',
            errors: 2,
            total: 10,
            accuracy: 80,
            trend: '↑',
            errorDetails: [
                { question: 4, userAnswer: 'C', correctAnswer: 'A' },
                { question: 7, userAnswer: 'D', correctAnswer: 'B' }
            ]
        },
        {
            course: 'C',
            practiceTime: '2024-10-24 09:15',
            errors: 4,
            total: 10,
            accuracy: 60,
            trend: '↓',
            errorDetails: [
                { question: 1, userAnswer: 'B', correctAnswer: 'C' },
                { question: 3, userAnswer: 'A', correctAnswer: 'D' },
                { question: 5, userAnswer: 'D', correctAnswer: 'A' },
                { question: 8, userAnswer: 'C', correctAnswer: 'B' }
            ]
        },
        {
            course: 'D',
            practiceTime: '2024-10-23 16:45',
            errors: 1,
            total: 10,
            accuracy: 90,
            trend: '↑',
            errorDetails: [
                { question: 6, userAnswer: 'A', correctAnswer: 'C' }
            ]
        },
        {
            course: 'E',
            practiceTime: '2024-10-22 11:20',
            errors: 5,
            total: 10,
            accuracy: 50,
            trend: '↓',
            errorDetails: [
                { question: 2, userAnswer: 'B', correctAnswer: 'A' },
                { question: 4, userAnswer: 'C', correctAnswer: 'D' },
                { question: 6, userAnswer: 'A', correctAnswer: 'B' },
                { question: 8, userAnswer: 'D', correctAnswer: 'C' },
                { question: 9, userAnswer: 'B', correctAnswer: 'A' }
            ]
        },
        {
            course: 'F',
            practiceTime: '2024-10-21 13:10',
            errors: 0,
            total: 10,
            accuracy: 100,
            trend: '↑',
            errorDetails: []
        }
    ];

    // 分頁設定
    let currentPage = 1;
    let itemsPerPage = 10;
    let filteredData = [...learningData];

    // 初始化
    function init() {
        renderTable();
        updatePagination();
        bindEvents();
        updateProgress();
        updateLearningBehavior();
    }

    // 渲染表格資料
    function renderTable() {
        const tbody = $('#error-stats-container');
        tbody.empty();

        const startIndex = (currentPage - 1) * itemsPerPage;
        const endIndex = Math.min(startIndex + itemsPerPage, filteredData.length);
        const pageData = filteredData.slice(startIndex, endIndex);

        if (pageData.length === 0) {
            tbody.append(`
                <tr>
                    <td colspan="6" class="text-center">沒有找到相關資料</td>
                </tr>
            `);
            return;
        }

        pageData.forEach((item, index) => {
            const errorDetailsText = item.errorDetails.length > 0 ? 
                item.errorDetails.map(error => 
                    `題目 ${error.question} 您的答案為 ${error.userAnswer} 正確答案為 ${error.correctAnswer}`
                ).join('　') : '無錯誤';

            const trendClass = item.trend === '↑' ? 'trend-up' : 
                              item.trend === '↓' ? 'trend-down' : '';

            const rowClass = (startIndex + index) % 2 === 0 ? 'odd' : 'even';

            tbody.append(`
                <tr class="${rowClass}">
                    <td class="sorting_1">${item.course}</td>
                    <td>${item.practiceTime}</td>
                    <td>${item.errors}/${item.total}</td>
                    <td>${item.accuracy}%</td>
                    <td><span class="trend-arrow ${trendClass}">${item.trend}</span></td>
                    <td>${errorDetailsText}</td>
                </tr>
            `);
        });

        // 更新顯示資訊
        updateTableInfo();
    }

    // 更新表格資訊
    function updateTableInfo() {
        const startIndex = Math.min((currentPage - 1) * itemsPerPage + 1, filteredData.length);
        const endIndex = Math.min(currentPage * itemsPerPage, filteredData.length);
        const total = filteredData.length;

        if (total === 0) {
            $('#dataTable_info').text('Showing 0 to 0 of 0 entries');
        } else {
            $('#dataTable_info').text(`Showing ${startIndex} to ${endIndex} of ${total} entries`);
        }
    }

    // 更新分頁按鈕
    function updatePagination() {
        const totalPages = Math.ceil(filteredData.length / itemsPerPage);
        const pagination = $('.pagination');
        
        // 清空現有分頁按鈕（保留 Previous 和 Next）
        pagination.find('li:not(#dataTable_previous):not(#dataTable_next)').remove();

        // 更新 Previous 按鈕狀態
        const prevBtn = $('#dataTable_previous');
        if (currentPage === 1) {
            prevBtn.addClass('disabled');
        } else {
            prevBtn.removeClass('disabled');
        }

        // 計算要顯示的頁碼範圍
        let startPage = Math.max(1, currentPage - 2);
        let endPage = Math.min(totalPages, startPage + 4);
        
        if (endPage - startPage < 4) {
            startPage = Math.max(1, endPage - 4);
        }

        // 產生頁碼按鈕
        for (let i = startPage; i <= endPage; i++) {
            const isActive = i === currentPage ? 'active' : '';
            const pageBtn = `
                <li class="paginate_button page-item ${isActive}">
                    <a href="#" aria-controls="dataTable" data-dt-idx="${i}" tabindex="0" class="page-link">${i}</a>
                </li>
            `;
            $('#dataTable_next').before(pageBtn);
        }

        // 更新 Next 按鈕狀態
        const nextBtn = $('#dataTable_next');
        if (currentPage === totalPages || totalPages === 0) {
            nextBtn.addClass('disabled');
        } else {
            nextBtn.removeClass('disabled');
        }
    }

    // 搜尋功能
    function handleSearch(searchTerm) {
        filteredData = learningData.filter(item => 
            item.course.toLowerCase().includes(searchTerm.toLowerCase()) ||
            item.practiceTime.includes(searchTerm)
        );
        currentPage = 1;
        renderTable();
        updatePagination();
    }

    // 更新每頁顯示數量
    function handlePageSizeChange(newSize) {
        itemsPerPage = parseInt(newSize);
        currentPage = 1;
        renderTable();
        updatePagination();
    }

    // 分頁點擊處理
    function handlePageClick(page) {
        if (page === 'prev' && currentPage > 1) {
            currentPage--;
        } else if (page === 'next') {
            const totalPages = Math.ceil(filteredData.length / itemsPerPage);
            if (currentPage < totalPages) {
                currentPage++;
            }
        } else if (typeof page === 'number') {
            currentPage = page;
        }
        renderTable();
        updatePagination();
    }

    // 綁定事件
    function bindEvents() {
        // 搜尋框事件
        $('#dataTable_filter input').on('input', function() {
            const searchTerm = $(this).val();
            handleSearch(searchTerm);
        });

        // 每頁顯示數量變更事件
        $('select[name="dataTable_length"]').on('change', function() {
            const newSize = $(this).val();
            handlePageSizeChange(newSize);
        });

        // 分頁按鈕點擊事件 - 使用事件委派處理動態生成的按鈕
        $(document).on('click', '.paginate_button:not(.disabled) a', function(e) {
            e.preventDefault();
            const $this = $(this);
            const parent = $this.parent();

            // 移除所有 active 狀態
            $('.paginate_button').removeClass('active');

            if (parent.attr('id') === 'dataTable_previous') {
                handlePageClick('prev');
            } else if (parent.attr('id') === 'dataTable_next') {
                handlePageClick('next');
            } else {
                const page = parseInt($this.attr('data-dt-idx'));
                parent.addClass('active');
                handlePageClick(page);
            }
        });

        // 表格排序功能（簡單實作）
        $('.sorting').on('click', function() {
            const columnIndex = $(this).index();
            const isAsc = $(this).hasClass('sorting_asc');
            
            // 移除所有排序 class
            $('.sorting').removeClass('sorting_asc sorting_desc').addClass('sorting');
            
            // 設定當前欄位排序
            if (isAsc) {
                $(this).removeClass('sorting').addClass('sorting_desc');
                sortData(columnIndex, 'desc');
            } else {
                $(this).removeClass('sorting').addClass('sorting_asc');
                sortData(columnIndex, 'asc');
            }
        });
    }

    // 排序功能
    function sortData(columnIndex, direction) {
        const sortKeys = ['course', 'practiceTime', 'errors', 'accuracy', 'trend', 'errorDetails'];
        const key = sortKeys[columnIndex];

        filteredData.sort((a, b) => {
            let valueA = a[key];
            let valueB = b[key];

            // 特殊處理不同類型的資料
            if (key === 'errors') {
                valueA = a.errors;
                valueB = b.errors;
            } else if (key === 'accuracy') {
                valueA = a.accuracy;
                valueB = b.accuracy;
            } else if (key === 'practiceTime') {
                valueA = new Date(a.practiceTime);
                valueB = new Date(b.practiceTime);
            }

            if (direction === 'asc') {
                return valueA > valueB ? 1 : -1;
            } else {
                return valueA < valueB ? 1 : -1;
            }
        });

        currentPage = 1;
        renderTable();
        updatePagination();
    }

    // 更新學習進度
    function updateProgress() {
        // 課程進度
        const completedCourses = 4; // 假設完成了4個課程
        const totalCourses = 9;
        const courseProgress = Math.round((completedCourses / totalCourses) * 100);
        
        $('.progress-bar.bg-info').css('width', courseProgress + '%').attr('aria-valuenow', courseProgress);
        $('#course-progress-description').text(`目前學到課程 ${String.fromCharCode(65 + completedCourses - 1)}，完成度 ${courseProgress}%`);

        // 練習正確率
        const totalAccuracy = learningData.reduce((sum, item) => sum + item.accuracy, 0);
        const averageAccuracy = Math.round(totalAccuracy / learningData.length);
        
        $('.progress-bar.bg-success').css('width', averageAccuracy + '%').attr('aria-valuenow', averageAccuracy);
        $('#exercise-progress-description').text(`平均正確率：${averageAccuracy}% (已完成 ${learningData.length}/${totalCourses} 個練習)`);
    }

    // 更新學習行為分析
    function updateLearningBehavior() {
        const behaviorList = $('#learning-behavior-description');
        behaviorList.empty();

        const behaviors = [
            '平均每週練習 3 次',
            '最常練習時段：下午 2-5 點',
            '連續學習天數：7 天',
            '最擅長課程：F (100% 正確率)',
            '需要加強課程：E (50% 正確率)'
        ];

        behaviors.forEach(behavior => {
            behaviorList.append(`<li>${behavior}</li>`);
        });

        // 更新建議原因
        const adviceList = $('#advice-reasons');
        adviceList.empty();

        const reasons = [
            '課程 E 錯誤率較高，建議重新複習基礎概念',
            '課程 C 有退步趨勢，可能需要額外練習',
            '課程 F 表現優異，可以嘗試進階內容'
        ];

        reasons.forEach(reason => {
            adviceList.append(`<li>${reason}</li>`);
        });
    }

    // 啟動初始化
    init();
});
