SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;


DROP TABLE IF EXISTS `bioreads`;
CREATE TABLE `bioreads` (
  `readid` int(11) NOT NULL,
  `userid` int(11) DEFAULT NULL,
  `pressure` varchar(100) DEFAULT NULL,
  `heartrate` varchar(100) DEFAULT NULL,
  `temper` varchar(100) DEFAULT NULL,
  `age` varchar(110) DEFAULT NULL,
  `predicts` varchar(250) DEFAULT NULL,
  `doccomment` mediumtext DEFAULT NULL,
  `readtime` int(11) DEFAULT NULL
) ENGINE=MyISAM DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

INSERT INTO `bioreads` (`readid`, `userid`, `pressure`, `heartrate`, `temper`, `age`, `predicts`, `doccomment`, `readtime`) VALUES
(1, 9, '92', '112', '35', '12', NULL, NULL, 1744467535);

DROP TABLE IF EXISTS `userroles`;
CREATE TABLE `userroles` (
  `roleid` int(11) NOT NULL,
  `rolename` varchar(250) DEFAULT NULL
) ENGINE=MyISAM DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

INSERT INTO `userroles` (`roleid`, `rolename`) VALUES
(1, 'Administrators'),
(2, 'Doctors'),
(3, 'Patients');

DROP TABLE IF EXISTS `users`;
CREATE TABLE `users` (
  `userid` int(11) NOT NULL,
  `roleid` int(11) DEFAULT NULL,
  `username` varchar(250) DEFAULT NULL,
  `password` varchar(250) DEFAULT NULL,
  `fullname` varchar(250) DEFAULT NULL,
  `email` varchar(250) DEFAULT NULL,
  `mobile` varchar(12) DEFAULT NULL,
  `nat_id` varchar(50) DEFAULT NULL,
  `gender` varchar(11) DEFAULT NULL
) ENGINE=MyISAM DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

INSERT INTO `users` (`userid`, `roleid`, `username`, `password`, `fullname`, `email`, `mobile`, `nat_id`, `gender`) VALUES
(1, 1, 'admin', 'admin', 'admin', 'admin@localhost.com', NULL, NULL, NULL),
(2, 2, 'aaa', 'aaa', 'Shahad ', 'aaa@aaa.com', '5555555', '1111963598', '1'),
(8, 3, 'sss', 'sss', 'Shahad ', 'aaa@aaa.com', '5555555', '1111963598', '1'),
(9, 3, 'ccc', 'ccc', 'ccc', 'ccc@ccc.com', '3333', '444', '1');


ALTER TABLE `bioreads`
  ADD PRIMARY KEY (`readid`);

ALTER TABLE `userroles`
  ADD PRIMARY KEY (`roleid`);

ALTER TABLE `users`
  ADD PRIMARY KEY (`userid`);


ALTER TABLE `bioreads`
  MODIFY `readid` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

ALTER TABLE `userroles`
  MODIFY `roleid` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

ALTER TABLE `users`
  MODIFY `userid` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=10;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
