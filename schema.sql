
/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;


CREATE TABLE IF NOT EXISTS `alembic_version` (
  `version_num` varchar(32) NOT NULL
) TYPE=MyISAM;

CREATE TABLE IF NOT EXISTS `bank_account` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `account_name` varchar(255) DEFAULT NULL,
  `is_personal` tinyint(1) DEFAULT '0',
  `is_primary` tinyint(1) DEFAULT '0',
  `bank_name` varchar(255) DEFAULT NULL,
  `number` varchar(100) DEFAULT NULL,
  `sort_code` varchar(100) DEFAULT NULL,
  `show_on_invoice` tinyint(1) DEFAULT '1',
  `created_at` datetime NOT NULL,
  `updated_at` datetime NOT NULL,
  PRIMARY KEY (`id`),
  KEY `user_id_idx` (`user_id`)
) TYPE=InnoDB AUTO_INCREMENT=1 ;

CREATE TABLE IF NOT EXISTS `company` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `logo_id` int(11) DEFAULT NULL,
  `company_type_id` int(11) DEFAULT NULL,
  `name` varchar(255) DEFAULT NULL,
  `address1` varchar(255) DEFAULT NULL,
  `address2` varchar(255) DEFAULT NULL,
  `town` varchar(100) NOT NULL,
  `city` varchar(255) DEFAULT NULL,
  `county` varchar(255) DEFAULT NULL,
  `country` varchar(3) NOT NULL,
  `post_code` varchar(20) DEFAULT NULL,
  `registration_number` varchar(30) DEFAULT NULL,
  `created_at` datetime NOT NULL,
  `updated_at` datetime NOT NULL,
  PRIMARY KEY (`id`),
  KEY `user_id_idx` (`user_id`),
  KEY `company_type_id_idx` (`company_type_id`),
  KEY `logo_id_idx` (`logo_id`)
) TYPE=InnoDB  AUTO_INCREMENT=4 ;

CREATE TABLE IF NOT EXISTS `company_type` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(100) DEFAULT NULL,
  `created_at` datetime NOT NULL,
  `updated_at` datetime NOT NULL,
  PRIMARY KEY (`id`)
) TYPE=InnoDB  AUTO_INCREMENT=5 ;

CREATE TABLE IF NOT EXISTS `contact` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `first_name` varchar(255) DEFAULT NULL,
  `last_name` varchar(255) DEFAULT NULL,
  `organisation` varchar(255) DEFAULT NULL,
  `email_address` varchar(255) DEFAULT NULL,
  `billing_email_address` varchar(255) DEFAULT NULL,
  `address_line1` varchar(255) DEFAULT NULL,
  `address_line2` varchar(255) DEFAULT NULL,
  `town` varchar(255) DEFAULT NULL,
  `city` varchar(255) DEFAULT NULL,
  `county` varchar(255) DEFAULT NULL,
  `country` varchar(2) DEFAULT NULL,
  `post_code` varchar(15) DEFAULT NULL,
  `created_at` datetime NOT NULL,
  `updated_at` datetime NOT NULL,
  PRIMARY KEY (`id`),
  KEY `user_id_idx` (`user_id`)
) TYPE=InnoDB  AUTO_INCREMENT=9 ;

CREATE TABLE IF NOT EXISTS `country` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `iso` varchar(2) DEFAULT NULL,
  `name` varchar(80) DEFAULT NULL,
  `printable_name` varchar(80) DEFAULT NULL,
  `iso3` varchar(3) DEFAULT NULL,
  PRIMARY KEY (`id`)
) TYPE=InnoDB  AUTO_INCREMENT=240 ;

CREATE TABLE IF NOT EXISTS `currency` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `code` varchar(6) DEFAULT NULL,
  `symbol` varchar(6) DEFAULT NULL,
  `name` varchar(50) DEFAULT NULL,
  `created_at` datetime NOT NULL,
  `updated_at` datetime NOT NULL,
  PRIMARY KEY (`id`),
  KEY `idx_code_idx` (`code`)
) TYPE=InnoDB  AUTO_INCREMENT=6 ;

CREATE TABLE IF NOT EXISTS `file` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `filename` varchar(255) DEFAULT NULL,
  `filesize` int(11) DEFAULT NULL,
  `extension` varchar(25) DEFAULT NULL,
  `mimetype` varchar(255) DEFAULT NULL,
  `location` varchar(255) DEFAULT NULL,
  `width` int(11) DEFAULT NULL,
  `height` int(11) DEFAULT NULL,
  `hash` varchar(40) DEFAULT NULL,
  `created_at` datetime NOT NULL,
  `updated_at` datetime NOT NULL,
  PRIMARY KEY (`id`)
) TYPE=InnoDB  AUTO_INCREMENT=33 ;

CREATE TABLE IF NOT EXISTS `forgot_password` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `unique_key` varchar(255) DEFAULT NULL,
  `expires_at` datetime NOT NULL,
  `created_at` datetime NOT NULL,
  `updated_at` datetime NOT NULL,
  PRIMARY KEY (`id`),
  KEY `user_id_idx` (`user_id`)
) TYPE=InnoDB AUTO_INCREMENT=1 ;

CREATE TABLE IF NOT EXISTS `group` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) DEFAULT NULL,
  `description` text,
  `created_at` datetime NOT NULL,
  `updated_at` datetime NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) TYPE=InnoDB AUTO_INCREMENT=1 ;

CREATE TABLE IF NOT EXISTS `invoice` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) DEFAULT NULL,
  `contact_id` int(11) DEFAULT NULL,
  `payment_term_id` int(11) DEFAULT NULL,
  `status` varchar(255) DEFAULT 'draft',
  `reference` varchar(255) DEFAULT NULL,
  `po_reference` varchar(255) DEFAULT NULL,
  `currency_code` varchar(5) DEFAULT NULL,
  `date_issued` datetime DEFAULT NULL,
  `due_date` datetime DEFAULT NULL,
  `written_off_date` datetime DEFAULT NULL,
  `sub_total` decimal(8,2) DEFAULT NULL,
  `tax` decimal(8,2) DEFAULT NULL,
  `total` decimal(8,2) DEFAULT NULL,
  `created_at` datetime NOT NULL,
  `updated_at` datetime NOT NULL,
  PRIMARY KEY (`id`),
  KEY `user_id_idx` (`user_id`),
  KEY `contact_id_idx` (`contact_id`),
  KEY `payment_term_id_idx` (`payment_term_id`)
) TYPE=InnoDB  AUTO_INCREMENT=14 ;

CREATE TABLE IF NOT EXISTS `invoice_item` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `invoice_id` int(11) DEFAULT NULL,
  `type_id` int(11) DEFAULT NULL,
  `tax_rate_id` int(11) DEFAULT NULL,
  `description` text,
  `quantity` decimal(5,3) DEFAULT NULL,
  `price` decimal(8,2) DEFAULT NULL,
  `tax` decimal(8,2) DEFAULT NULL,
  `total` decimal(8,2) DEFAULT NULL,
  `sort_order` mediumint(9) DEFAULT NULL,
  `created_at` datetime NOT NULL,
  `updated_at` datetime NOT NULL,
  PRIMARY KEY (`id`),
  KEY `invoice_id_idx` (`invoice_id`),
  KEY `type_id_idx` (`type_id`),
  KEY `tax_rate_id_idx` (`tax_rate_id`)
) TYPE=InnoDB  AUTO_INCREMENT=33 ;

CREATE TABLE IF NOT EXISTS `invoice_item_type` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(20) DEFAULT NULL,
  `name_plural` varchar(20) NOT NULL,
  `sort_order` mediumint(9) DEFAULT NULL,
  `created_at` datetime NOT NULL,
  `updated_at` datetime NOT NULL,
  PRIMARY KEY (`id`)
) TYPE=InnoDB  AUTO_INCREMENT=15 ;

CREATE TABLE IF NOT EXISTS `logo` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `original_image_id` int(11) NOT NULL,
  `thumbnail_image_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `original_image_id` (`original_image_id`),
  KEY `thumbnail_image_id` (`thumbnail_image_id`)
) TYPE=InnoDB  AUTO_INCREMENT=2 ;

CREATE TABLE IF NOT EXISTS `payment_term` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(50) DEFAULT NULL,
  `days` mediumint(9) DEFAULT NULL,
  `created_at` datetime NOT NULL,
  `updated_at` datetime NOT NULL,
  PRIMARY KEY (`id`)
) TYPE=InnoDB  AUTO_INCREMENT=7 ;

CREATE TABLE IF NOT EXISTS `tax_rate` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` bigint(11) NOT NULL,
  `type` varchar(255) DEFAULT 'VAT',
  `name` varchar(100) DEFAULT NULL,
  `rate` decimal(5,2) DEFAULT NULL,
  `created_at` datetime NOT NULL,
  `updated_at` datetime NOT NULL,
  PRIMARY KEY (`id`)
) TYPE=InnoDB  AUTO_INCREMENT=4 ;

CREATE TABLE IF NOT EXISTS `user` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `first_name` varchar(255) DEFAULT NULL,
  `last_name` varchar(255) DEFAULT NULL,
  `email_address` varchar(255) NOT NULL,
  `username` varchar(128) NOT NULL,
  `password` varchar(128) DEFAULT NULL,
  `is_active_account` tinyint(1) DEFAULT '1',
  `is_super_admin` tinyint(1) DEFAULT '0',
  `last_login` datetime DEFAULT NULL,
  `created_at` datetime NOT NULL,
  `updated_at` datetime NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `email_address` (`email_address`),
  UNIQUE KEY `username` (`username`),
  KEY `is_active_idx_idx` (`is_active_account`)
) TYPE=InnoDB  AUTO_INCREMENT=4 ;

CREATE TABLE IF NOT EXISTS `user_group` (
  `user_id` int(11) NOT NULL DEFAULT '0',
  `group_id` int(11) NOT NULL DEFAULT '0',
  `created_at` datetime NOT NULL,
  `updated_at` datetime NOT NULL,
  PRIMARY KEY (`user_id`,`group_id`),
  KEY `sf_guard_user_group_group_id_sf_guard_group_id` (`group_id`)
) TYPE=InnoDB;

CREATE TABLE IF NOT EXISTS `vat_registration` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `status` varchar(255) DEFAULT 'na',
  `number` varchar(20) DEFAULT NULL,
  `registration_date` datetime DEFAULT NULL,
  `de_registration_date` datetime DEFAULT NULL,
  `first_return_date` datetime DEFAULT NULL,
  `scheme_id` int(11) DEFAULT NULL,
  `created_at` datetime NOT NULL,
  `updated_at` datetime NOT NULL,
  PRIMARY KEY (`id`),
  KEY `scheme_id_idx` (`scheme_id`),
  KEY `user_id_idx` (`user_id`)
) TYPE=InnoDB AUTO_INCREMENT=1 ;

CREATE TABLE IF NOT EXISTS `vat_scheme` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(100) DEFAULT NULL,
  `vat_rate` decimal(5,2) DEFAULT NULL,
  `created_at` datetime NOT NULL,
  `updated_at` datetime NOT NULL,
  PRIMARY KEY (`id`)
) TYPE=InnoDB  AUTO_INCREMENT=56 ;


ALTER TABLE `bank_account`
  ADD CONSTRAINT `bank_account_user_id_sf_guard_user_id` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`) ON DELETE CASCADE;

ALTER TABLE `company`
  ADD CONSTRAINT `company_type_id_company_type_id` FOREIGN KEY (`company_type_id`) REFERENCES `company_type` (`id`) ON DELETE SET NULL,
  ADD CONSTRAINT `user_id_sf_guard_user_id` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`) ON DELETE CASCADE,
  ADD CONSTRAINT `company_logo_id_logo_id` FOREIGN KEY (`logo_id`) REFERENCES `logo` (`id`) ON DELETE SET NULL;

ALTER TABLE `contact`
  ADD CONSTRAINT `contact_user_id_sf_guard_user_id` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`) ON DELETE CASCADE;

ALTER TABLE `forgot_password`
  ADD CONSTRAINT `sf_guard_forgot_password_user_id_sf_guard_user_id` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`) ON DELETE CASCADE;

ALTER TABLE `invoice`
  ADD CONSTRAINT `invoice_contact_id_contact_id` FOREIGN KEY (`contact_id`) REFERENCES `contact` (`id`) ON DELETE SET NULL,
  ADD CONSTRAINT `invoice_payment_term_id_payment_term_id` FOREIGN KEY (`payment_term_id`) REFERENCES `payment_term` (`id`) ON DELETE SET NULL,
  ADD CONSTRAINT `invoice_user_id_sf_guard_user_id` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`) ON DELETE CASCADE;

ALTER TABLE `invoice_item`
  ADD CONSTRAINT `invoice_item_invoice_id_invoice_id` FOREIGN KEY (`invoice_id`) REFERENCES `invoice` (`id`) ON DELETE CASCADE,
  ADD CONSTRAINT `invoice_item_tax_rate_id_tax_rate_id` FOREIGN KEY (`tax_rate_id`) REFERENCES `tax_rate` (`id`) ON DELETE SET NULL,
  ADD CONSTRAINT `invoice_item_type_id_invoice_item_type_id` FOREIGN KEY (`type_id`) REFERENCES `invoice_item_type` (`id`) ON DELETE SET NULL;

ALTER TABLE `user_group`
  ADD CONSTRAINT `sf_guard_user_group_group_id_sf_guard_group_id` FOREIGN KEY (`group_id`) REFERENCES `group` (`id`) ON DELETE CASCADE,
  ADD CONSTRAINT `sf_guard_user_group_user_id_sf_guard_user_id` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`) ON DELETE CASCADE;

ALTER TABLE `vat_registration`
  ADD CONSTRAINT `vat_registration_scheme_id_vat_scheme_id` FOREIGN KEY (`scheme_id`) REFERENCES `vat_scheme` (`id`) ON DELETE SET NULL,
  ADD CONSTRAINT `vat_registration_user_id_sf_guard_user_id` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`) ON DELETE CASCADE;
