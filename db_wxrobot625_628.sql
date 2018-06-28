# Host: 127.0.0.1  (Version: 5.5.53)
# Date: 2018-06-28 23:34:49
# Generator: MySQL-Front 5.3  (Build 4.234)

/*!40101 SET NAMES utf8 */;

use db_wxrobot625;
use db_wxrobot625;

#
# Structure for table "tb_article"
#




DROP TABLE IF EXISTS `tb_article`;
CREATE TABLE `tb_article` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `article_name` varchar(100) COLLATE utf8mb4_bin NOT NULL,
  `article_title` varchar(256) COLLATE utf8mb4_bin NOT NULL DEFAULT '',
  `article_url` varchar(256) CHARACTER SET utf8mb4 NOT NULL DEFAULT '',
  `read` int(11) DEFAULT '0',
  `like` int(11) NOT NULL DEFAULT '0',
  `last_edit_time` varchar(10) COLLATE utf8mb4_bin NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=28 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin;

#
# Structure for table "tb_group"
#

DROP TABLE IF EXISTS `tb_group`;
CREATE TABLE `tb_group` (
  `group_id` int(11) NOT NULL AUTO_INCREMENT,
  `group_name` varchar(100) COLLATE utf8mb4_bin NOT NULL DEFAULT '',
  `number` int(5) NOT NULL DEFAULT '1' COMMENT '群人数',
  PRIMARY KEY (`group_id`),
  UNIQUE KEY `group_name` (`group_name`)
) ENGINE=InnoDB AUTO_INCREMENT=25 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin;

#
# Structure for table "tb_message"
#

DROP TABLE IF EXISTS `tb_message`;
CREATE TABLE `tb_message` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `group_id` int(11) NOT NULL,
  `member` varchar(100) CHARACTER SET utf8mb4 NOT NULL COMMENT '发言人',
  `text` varchar(10000) COLLATE utf8mb4_bin DEFAULT '',
  `picture` varchar(256) CHARACTER SET utf8mb4 DEFAULT NULL,
  `recording` varchar(256) CHARACTER SET utf8mb4 DEFAULT NULL,
  `duration` int(11) DEFAULT '0',
  `create_time` varchar(20) CHARACTER SET utf8mb4 DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=705 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin;
