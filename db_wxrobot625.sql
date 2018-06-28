# Host: 127.0.0.1  (Version: 5.5.53)
# Date: 2018-06-26 13:41:42
# Generator: MySQL-Front 5.3  (Build 4.234)

/*!40101 SET NAMES utf8 */;

#
# Structure for table "tb_group"
#

DROP TABLE IF EXISTS `tb_group`;
CREATE TABLE `tb_group` (
  `group_id` int(11) NOT NULL AUTO_INCREMENT,
  `group_name` varchar(100) NOT NULL,
  `number` varchar(5) NOT NULL DEFAULT '1' COMMENT '群人数',
  PRIMARY KEY (`group_id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;

#
# Data for table "tb_group"
#

/*!40000 ALTER TABLE `tb_group` DISABLE KEYS */;
/*!40000 ALTER TABLE `tb_group` ENABLE KEYS */;

#
# Structure for table "tb_message"
#

DROP TABLE IF EXISTS `tb_message`;
CREATE TABLE `tb_message` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `group_id` int(11) NOT NULL,
  `member` varchar(100) NOT NULL COMMENT '发言人',
  `text` mediumtext,
  `picture` varchar(256) DEFAULT NULL,
  `recording` varchar(256) DEFAULT NULL,
  `duratio` int(11) DEFAULT '0',
  `create_time` varchar(20) DEFAULT NULL,
  `group_name` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;

#
# Data for table "tb_message"
#

/*!40000 ALTER TABLE `tb_message` DISABLE KEYS */;
/*!40000 ALTER TABLE `tb_message` ENABLE KEYS */;
