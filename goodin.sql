-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- 主機： 127.0.0.1
-- 產生時間： 2025-06-29 11:25:49
-- 伺服器版本： 10.4.32-MariaDB
-- PHP 版本： 8.2.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- 資料庫： `goodin`
--

-- --------------------------------------------------------

--
-- 資料表結構 `course`
--

CREATE TABLE `course` (
  `course_id` int(11) NOT NULL,
  `title` varchar(100) DEFAULT NULL,
  `context` text DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- 資料表結構 `course_img`
--

CREATE TABLE `course_img` (
  `img_id` int(11) NOT NULL,
  `course_id` int(11) DEFAULT NULL,
  `img_url` varchar(255) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- 資料表結構 `exercise`
--

CREATE TABLE `exercise` (
  `exercise_id` int(11) NOT NULL,
  `course_id` int(11) DEFAULT NULL,
  `question_text` text DEFAULT NULL,
  `answer` text DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- 資料表結構 `exercise_img`
--

CREATE TABLE `exercise_img` (
  `img_id` int(11) NOT NULL,
  `exercise_id` int(11) DEFAULT NULL,
  `img_url` varchar(255) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- 資料表結構 `follow_stocks`
--

CREATE TABLE `follow_stocks` (
  `user_id` int(11) NOT NULL,
  `stock_id` int(11) NOT NULL,
  `follow_time` datetime DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- 資料表結構 `history_stock`
--

CREATE TABLE `history_stock` (
  `price_id` int(11) NOT NULL,
  `stock_id` int(11) DEFAULT NULL,
  `time` datetime DEFAULT NULL,
  `open` decimal(10,2) DEFAULT NULL,
  `high` decimal(10,2) DEFAULT NULL,
  `low` decimal(10,2) DEFAULT NULL,
  `close` decimal(10,2) DEFAULT NULL,
  `volume` bigint(20) DEFAULT NULL,
  `interval_type` enum('5min','15min','1h','4h','1d','1w') DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- 資料表結構 `holdings`
--

CREATE TABLE `holdings` (
  `holding_id` int(11) NOT NULL,
  `account_id` int(11) DEFAULT NULL,
  `stock_id` int(11) DEFAULT NULL,
  `quantity` int(11) DEFAULT NULL,
  `purchase_price` decimal(10,2) DEFAULT NULL,
  `last_updated` datetime DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- 資料表結構 `orders`
--

CREATE TABLE `orders` (
  `order_id` int(11) NOT NULL,
  `account_id` int(11) DEFAULT NULL,
  `stock_id` int(11) DEFAULT NULL,
  `order_type` varchar(10) DEFAULT NULL,
  `quantity` int(11) DEFAULT NULL,
  `order_price` decimal(10,2) DEFAULT NULL,
  `order_time` datetime DEFAULT NULL,
  `mode` enum('realtime','backtest') DEFAULT 'realtime'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- 資料表結構 `realtime_stock`
--

CREATE TABLE `realtime_stock` (
  `price_id` int(11) NOT NULL,
  `stock_id` int(11) DEFAULT NULL,
  `time` datetime DEFAULT NULL,
  `open` decimal(10,2) DEFAULT NULL,
  `high` decimal(10,2) DEFAULT NULL,
  `low` decimal(10,2) DEFAULT NULL,
  `close` decimal(10,2) DEFAULT NULL,
  `volume` bigint(20) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- 資料表結構 `simulated_accounts`
--

CREATE TABLE `simulated_accounts` (
  `account_id` int(11) NOT NULL,
  `user_id` int(11) DEFAULT NULL,
  `account_type` varchar(20) DEFAULT NULL,
  `cash` decimal(15,2) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- 資料表結構 `stocks`
--

CREATE TABLE `stocks` (
  `stock_id` int(11) NOT NULL,
  `symbol` varchar(10) NOT NULL,
  `name` varchar(100) DEFAULT NULL,
  `sector` varchar(100) DEFAULT NULL,
  `last_price_id` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- 資料表結構 `study_progress`
--

CREATE TABLE `study_progress` (
  `user_id` int(11) NOT NULL,
  `course_id` int(11) NOT NULL,
  `lesson_progress` int(11) DEFAULT NULL,
  `exercise_progress` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- 資料表結構 `user`
--

CREATE TABLE `user` (
  `user_id` int(11) NOT NULL,
  `username` varchar(50) NOT NULL,
  `phone` int(20) NOT NULL,
  `email` varchar(100) NOT NULL,
  `password` varchar(100) NOT NULL,
  `personality_test_result` text DEFAULT NULL,
  `final_test_score` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- 已傾印資料表的索引
--

--
-- 資料表索引 `course`
--
ALTER TABLE `course`
  ADD PRIMARY KEY (`course_id`);

--
-- 資料表索引 `course_img`
--
ALTER TABLE `course_img`
  ADD PRIMARY KEY (`img_id`),
  ADD KEY `course_id` (`course_id`);

--
-- 資料表索引 `exercise`
--
ALTER TABLE `exercise`
  ADD PRIMARY KEY (`exercise_id`),
  ADD KEY `course_id` (`course_id`);

--
-- 資料表索引 `exercise_img`
--
ALTER TABLE `exercise_img`
  ADD PRIMARY KEY (`img_id`),
  ADD KEY `exercise_id` (`exercise_id`);

--
-- 資料表索引 `follow_stocks`
--
ALTER TABLE `follow_stocks`
  ADD PRIMARY KEY (`user_id`,`stock_id`),
  ADD KEY `stock_id` (`stock_id`);

--
-- 資料表索引 `history_stock`
--
ALTER TABLE `history_stock`
  ADD PRIMARY KEY (`price_id`),
  ADD KEY `stock_id` (`stock_id`);

--
-- 資料表索引 `holdings`
--
ALTER TABLE `holdings`
  ADD PRIMARY KEY (`holding_id`),
  ADD KEY `account_id` (`account_id`),
  ADD KEY `stock_id` (`stock_id`);

--
-- 資料表索引 `orders`
--
ALTER TABLE `orders`
  ADD PRIMARY KEY (`order_id`),
  ADD KEY `account_id` (`account_id`),
  ADD KEY `stock_id` (`stock_id`);

--
-- 資料表索引 `realtime_stock`
--
ALTER TABLE `realtime_stock`
  ADD PRIMARY KEY (`price_id`),
  ADD KEY `stock_id` (`stock_id`);

--
-- 資料表索引 `simulated_accounts`
--
ALTER TABLE `simulated_accounts`
  ADD PRIMARY KEY (`account_id`),
  ADD KEY `user_id` (`user_id`);

--
-- 資料表索引 `stocks`
--
ALTER TABLE `stocks`
  ADD PRIMARY KEY (`stock_id`),
  ADD KEY `fk_last_price` (`last_price_id`);

--
-- 資料表索引 `study_progress`
--
ALTER TABLE `study_progress`
  ADD PRIMARY KEY (`user_id`,`course_id`),
  ADD KEY `course_id` (`course_id`);

--
-- 資料表索引 `user`
--
ALTER TABLE `user`
  ADD PRIMARY KEY (`user_id`);

--
-- 在傾印的資料表使用自動遞增(AUTO_INCREMENT)
--

--
-- 使用資料表自動遞增(AUTO_INCREMENT) `course`
--
ALTER TABLE `course`
  MODIFY `course_id` int(11) NOT NULL AUTO_INCREMENT;

--
-- 使用資料表自動遞增(AUTO_INCREMENT) `course_img`
--
ALTER TABLE `course_img`
  MODIFY `img_id` int(11) NOT NULL AUTO_INCREMENT;

--
-- 使用資料表自動遞增(AUTO_INCREMENT) `exercise`
--
ALTER TABLE `exercise`
  MODIFY `exercise_id` int(11) NOT NULL AUTO_INCREMENT;

--
-- 使用資料表自動遞增(AUTO_INCREMENT) `exercise_img`
--
ALTER TABLE `exercise_img`
  MODIFY `img_id` int(11) NOT NULL AUTO_INCREMENT;

--
-- 使用資料表自動遞增(AUTO_INCREMENT) `history_stock`
--
ALTER TABLE `history_stock`
  MODIFY `price_id` int(11) NOT NULL AUTO_INCREMENT;

--
-- 使用資料表自動遞增(AUTO_INCREMENT) `holdings`
--
ALTER TABLE `holdings`
  MODIFY `holding_id` int(11) NOT NULL AUTO_INCREMENT;

--
-- 使用資料表自動遞增(AUTO_INCREMENT) `orders`
--
ALTER TABLE `orders`
  MODIFY `order_id` int(11) NOT NULL AUTO_INCREMENT;

--
-- 使用資料表自動遞增(AUTO_INCREMENT) `realtime_stock`
--
ALTER TABLE `realtime_stock`
  MODIFY `price_id` int(11) NOT NULL AUTO_INCREMENT;

--
-- 使用資料表自動遞增(AUTO_INCREMENT) `simulated_accounts`
--
ALTER TABLE `simulated_accounts`
  MODIFY `account_id` int(11) NOT NULL AUTO_INCREMENT;

--
-- 使用資料表自動遞增(AUTO_INCREMENT) `stocks`
--
ALTER TABLE `stocks`
  MODIFY `stock_id` int(11) NOT NULL AUTO_INCREMENT;

--
-- 使用資料表自動遞增(AUTO_INCREMENT) `user`
--
ALTER TABLE `user`
  MODIFY `user_id` int(11) NOT NULL AUTO_INCREMENT;

--
-- 已傾印資料表的限制式
--

--
-- 資料表的限制式 `course_img`
--
ALTER TABLE `course_img`
  ADD CONSTRAINT `course_img_ibfk_1` FOREIGN KEY (`course_id`) REFERENCES `course` (`course_id`);

--
-- 資料表的限制式 `exercise`
--
ALTER TABLE `exercise`
  ADD CONSTRAINT `exercise_ibfk_1` FOREIGN KEY (`course_id`) REFERENCES `course` (`course_id`);

--
-- 資料表的限制式 `exercise_img`
--
ALTER TABLE `exercise_img`
  ADD CONSTRAINT `exercise_img_ibfk_1` FOREIGN KEY (`exercise_id`) REFERENCES `exercise` (`exercise_id`);

--
-- 資料表的限制式 `follow_stocks`
--
ALTER TABLE `follow_stocks`
  ADD CONSTRAINT `follow_stocks_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `user` (`user_id`),
  ADD CONSTRAINT `follow_stocks_ibfk_2` FOREIGN KEY (`stock_id`) REFERENCES `stocks` (`stock_id`);

--
-- 資料表的限制式 `history_stock`
--
ALTER TABLE `history_stock`
  ADD CONSTRAINT `history_stock_ibfk_1` FOREIGN KEY (`stock_id`) REFERENCES `stocks` (`stock_id`);

--
-- 資料表的限制式 `holdings`
--
ALTER TABLE `holdings`
  ADD CONSTRAINT `holdings_ibfk_1` FOREIGN KEY (`account_id`) REFERENCES `simulated_accounts` (`account_id`),
  ADD CONSTRAINT `holdings_ibfk_2` FOREIGN KEY (`stock_id`) REFERENCES `stocks` (`stock_id`);

--
-- 資料表的限制式 `orders`
--
ALTER TABLE `orders`
  ADD CONSTRAINT `orders_ibfk_1` FOREIGN KEY (`account_id`) REFERENCES `simulated_accounts` (`account_id`),
  ADD CONSTRAINT `orders_ibfk_2` FOREIGN KEY (`stock_id`) REFERENCES `stocks` (`stock_id`);

--
-- 資料表的限制式 `realtime_stock`
--
ALTER TABLE `realtime_stock`
  ADD CONSTRAINT `realtime_stock_ibfk_1` FOREIGN KEY (`stock_id`) REFERENCES `stocks` (`stock_id`);

--
-- 資料表的限制式 `simulated_accounts`
--
ALTER TABLE `simulated_accounts`
  ADD CONSTRAINT `simulated_accounts_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `user` (`user_id`);

--
-- 資料表的限制式 `study_progress`
--
ALTER TABLE `study_progress`
  ADD CONSTRAINT `study_progress_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `user` (`user_id`),
  ADD CONSTRAINT `study_progress_ibfk_2` FOREIGN KEY (`course_id`) REFERENCES `course` (`course_id`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
