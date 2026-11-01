-- MySQL dump 10.13  Distrib 8.0.46, for Win64 (x86_64)
--
-- Host: localhost    Database: movie_recommendation
-- ------------------------------------------------------
-- Server version	8.0.46

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `movies`
--

DROP TABLE IF EXISTS `movies`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `movies` (
  `movie_id` int NOT NULL AUTO_INCREMENT,
  `title` varchar(200) NOT NULL,
  `release_year` int DEFAULT NULL,
  `genre` varchar(100) NOT NULL,
  `poster_url` varchar(500) DEFAULT NULL,
  PRIMARY KEY (`movie_id`)
) ENGINE=InnoDB AUTO_INCREMENT=31 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `movies`
--

LOCK TABLES `movies` WRITE;
/*!40000 ALTER TABLE `movies` DISABLE KEYS */;
INSERT INTO `movies` VALUES (1,'RRR',2022,'Action','/static/poster/rrr.jpg'),(2,'Pushpa: The Rise',2021,'Action','/static/poster/pushpa.jpg'),(3,'Baahubali: The Beginning',2015,'Action','/static/poster/bahubali.jpg'),(4,'Salaar: Part 1 - Ceasefire',2023,'Action','/static/poster/salaar.jpg'),(5,'Rangasthalam',2018,'Drama','/static/poster/rangasthalam.jpg'),(6,'Sita Ramam',2022,'Romance','/static/poster/sitaramam.jpg'),(7,'Hi Nanna',2023,'Drama','/static/poster/hinanna.jpg'),(8,'Bommarillu',2006,'Romance','/static/poster/b.jpg'),(9,'Geetha Govindam',2018,'Romance','/static/poster/geethagovindam.jpg'),(10,'Jersey',2019,'Drama','/static/poster/jersey.jpg'),(11,'Jathi Ratnalu',2021,'Comedy','/static/poster/jathiratnalu.jpg'),(12,'F2: Fun and Frustration',2019,'Comedy','/static/poster/f2.jpg'),(13,'Nuvvu Naaku Nachav',2001,'Comedy','/static/poster/nuvvunaakNachav.jpg'),(14,'MAD',2023,'Comedy','/static/poster/mad.jpg'),(15,'Aha Naa Pellanta',1987,'Comedy','/static/poster/ahana.jpg'),(16,'HIT: The First Case',2020,'Thriller','/static/poster/hit.jpg'),(17,'Agent Sai Srinivasa Athreya',2019,'Mystery','/static/poster/assa.jpg'),(18,'Evaru',2019,'Thriller','/static/poster/evaru.jpg'),(19,'Kshanam',2016,'Mystery','/static/poster/kshanam.jpg'),(20,'Drushyam',2014,'Thriller','/static/poster/d,jpg.webp'),(21,'Bhaagamathie',2018,'Horror','/static/poster/bha.jpg'),(22,'Arundhati',2009,'Horror','/static/poster/aru,jpg.webp'),(23,'Masooda',2022,'Horror','/static/poster/masooda.jpg'),(24,'Virupaksha',2023,'Horror','/static/poster/virupaksha.jpg'),(25,'Ekkadiki Pothavu Chinnavada',2016,'Fantasy','/static/poster/epc.jpg'),(26,'Aditya 369',1991,'Sci-Fi','/static/poster/aditya369.jpg'),(27,'Eega',2012,'Fantasy','/static/poster/Eega.jpg'),(28,'Kalki 2898 AD',2024,'Sci-Fi','/static/poster/kalki2898.jpg'),(29,'Awe!',2018,'Thriller','/static/poster/qwe.jpg'),(30,'Manam',2014,'Fantasy','/static/poster/manam.jpg');
/*!40000 ALTER TABLE `movies` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `ratings`
--

DROP TABLE IF EXISTS `ratings`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `ratings` (
  `rating_id` int NOT NULL AUTO_INCREMENT,
  `user_id` int NOT NULL,
  `movie_id` int NOT NULL,
  `rating` decimal(2,1) NOT NULL,
  `rated_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`rating_id`),
  UNIQUE KEY `user_id` (`user_id`,`movie_id`),
  KEY `movie_id` (`movie_id`),
  CONSTRAINT `ratings_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`user_id`),
  CONSTRAINT `ratings_ibfk_2` FOREIGN KEY (`movie_id`) REFERENCES `movies` (`movie_id`),
  CONSTRAINT `ratings_chk_1` CHECK (((`rating` >= 1) and (`rating` <= 5)))
) ENGINE=InnoDB AUTO_INCREMENT=44 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `ratings`
--

LOCK TABLES `ratings` WRITE;
/*!40000 ALTER TABLE `ratings` DISABLE KEYS */;
INSERT INTO `ratings` VALUES (1,1,1,5.0,'2026-10-22 07:13:24'),(2,1,2,4.5,'2026-10-22 07:13:24'),(3,1,3,4.0,'2026-10-22 07:13:24'),(4,1,6,5.0,'2026-10-22 07:13:24'),(5,1,9,4.5,'2026-10-22 07:13:24'),(6,2,1,4.5,'2026-10-22 07:13:24'),(7,2,4,5.0,'2026-10-22 07:13:24'),(8,2,5,5.0,'2026-10-22 07:57:11'),(9,2,7,4.5,'2026-10-22 07:13:24'),(10,2,11,5.0,'2026-10-22 07:13:24'),(11,3,6,5.0,'2026-10-22 07:13:24'),(12,3,8,4.5,'2026-10-22 07:13:24'),(13,3,9,4.0,'2026-10-22 07:13:24'),(14,3,10,5.0,'2026-10-22 07:13:24'),(15,3,12,4.5,'2026-10-22 07:13:24'),(16,4,11,5.0,'2026-10-22 07:13:24'),(17,4,12,4.5,'2026-10-22 07:13:24'),(18,4,13,5.0,'2026-10-22 07:13:24'),(19,4,14,4.0,'2026-10-22 07:13:24'),(20,4,15,4.5,'2026-10-22 07:13:24'),(21,5,16,5.0,'2026-10-22 07:13:24'),(22,5,17,4.5,'2026-10-22 07:13:24'),(23,5,18,5.0,'2026-10-22 07:13:24'),(24,5,19,4.0,'2026-10-22 07:13:24'),(25,5,20,4.5,'2026-10-22 07:13:24'),(27,1,4,4.5,'2026-10-22 09:09:20'),(30,6,27,3.0,'2026-10-23 10:12:15'),(33,9,18,3.0,'2026-10-24 12:44:08'),(34,9,27,4.0,'2026-10-24 12:44:17'),(35,9,21,3.5,'2026-10-24 12:46:22'),(36,10,15,3.0,'2026-10-26 04:12:34'),(37,10,16,1.0,'2026-10-26 04:12:54'),(38,10,11,3.0,'2026-10-26 04:13:18'),(39,11,22,4.0,'2026-10-26 06:34:43'),(40,6,4,4.0,'2026-10-26 12:06:36'),(42,6,2,2.0,'2026-10-26 14:42:03'),(43,6,1,3.0,'2026-10-26 14:42:23');
/*!40000 ALTER TABLE `ratings` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `user_genres`
--

DROP TABLE IF EXISTS `user_genres`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `user_genres` (
  `user_id` int NOT NULL,
  `genre` varchar(100) NOT NULL,
  PRIMARY KEY (`user_id`,`genre`),
  CONSTRAINT `user_genres_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`user_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `user_genres`
--

LOCK TABLES `user_genres` WRITE;
/*!40000 ALTER TABLE `user_genres` DISABLE KEYS */;
INSERT INTO `user_genres` VALUES (1,'Action'),(1,'Fantasy'),(2,'Comedy'),(2,'Romance'),(3,'Drama'),(3,'Romance'),(4,'Comedy'),(5,'Mystery'),(5,'Thriller'),(6,'Action'),(6,'Fantasy'),(10,'Comedy'),(10,'Drama'),(11,'Comedy');
/*!40000 ALTER TABLE `user_genres` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `users`
--

DROP TABLE IF EXISTS `users`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `users` (
  `user_id` int NOT NULL AUTO_INCREMENT,
  `display_name` varchar(100) NOT NULL,
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `username` varchar(50) DEFAULT NULL,
  `password_hash` varchar(255) DEFAULT NULL,
  `email` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`user_id`),
  UNIQUE KEY `username` (`username`)
) ENGINE=InnoDB AUTO_INCREMENT=13 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `users`
--

LOCK TABLES `users` WRITE;
/*!40000 ALTER TABLE `users` DISABLE KEYS */;
INSERT INTO `users` VALUES (1,'User1','2026-10-22 07:12:21',NULL,NULL,NULL),(2,'User2','2026-10-22 07:12:21',NULL,NULL,NULL),(3,'User3','2026-10-22 07:12:21',NULL,NULL,NULL),(4,'User4','2026-10-22 07:12:21',NULL,NULL,NULL),(5,'User5','2026-10-22 07:12:21',NULL,NULL,NULL),(6,'divya sree','2026-10-23 09:05:16','divya2008','scrypt:32768:8:1$ss15wWGWuU6eFMk0$46d22673bbb6415242c132b5dee4cc3a0e7fc630c4537d1853ff65636945755fe58280293632a36584b24c1c4c2734671c0841b70bf29eb7089e165a9fd75a87',NULL),(7,'amrutha','2026-10-24 12:42:06','123am','scrypt:32768:8:1$EWNsj2BiQ3G6PFrW$bb94471a58209d5522b904fceef538f92edea40bcc663a7188ffdcc4d3ef12c04053b67670f15d4c74c75c289c38215609e8665d402e03c658f46e9db5830cf2',NULL),(8,'amrutha','2026-10-24 12:42:27','ammu','scrypt:32768:8:1$PTWaxuxjJ8lHmxhz$7bce429a4feb0d8fe736bf36a7e00fcf1f169b0c07413b85374ffea050d17f18bca7c12ed81eadcf1890dc4feeb9be5b21c32577304c8af7ff0e5fb7e6993280',NULL),(9,'amrutha reddy','2026-10-24 12:43:38','ammmu','scrypt:32768:8:1$sgaFa6bmj6bm6tLD$f39e16d8a575cad6b93dd88aa58496b377149990819a27d6fa988265b22a71d43ca7087830a1da8c5254b3f42ba476074d55e7b8aa334e473df2573d380c1de8',NULL),(10,'neha','2026-10-26 04:11:28','neha2007','scrypt:32768:8:1$bugpvl49Z3imIrIh$24b57f9c208a86a6a320023e0dc22961456e31b571df08213b6ed74c4ca59eb788827b34ab8bbd19a8ea759da92154e4763d5f1acc0e38a693eb42212b1fc5d1',NULL),(11,'thejuu','2026-10-26 06:33:24','theju20','scrypt:32768:8:1$vEfauzroROYxrPen$a6e80c983fe2d8d19552ae951f078d938f32be4f4a7ed1b990f2a9627f309c31981455c451adc2f7eb0a3aa2c8109feadcf643b6e9072687726f5d53b0b043e4',NULL),(12,'pandu','2026-10-31 04:53:25','pandu2006','scrypt:32768:8:1$gOuSltRo3w6iCcNt$8b03bf486e694822d5a7dbbd42b6627ab4c5d484547ef8463238974dec5e97dc90f4fe0debcb6186c62e10fd93671b5fb5f7c932c3e4653149b9fa639c64267c','tadimarrid@gmail.com');
/*!40000 ALTER TABLE `users` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `watchlist`
--

DROP TABLE IF EXISTS `watchlist`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `watchlist` (
  `watchlist_id` int NOT NULL AUTO_INCREMENT,
  `user_id` int NOT NULL,
  `movie_id` int NOT NULL,
  `added_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`watchlist_id`),
  UNIQUE KEY `user_id` (`user_id`,`movie_id`),
  KEY `movie_id` (`movie_id`),
  CONSTRAINT `watchlist_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`user_id`) ON DELETE CASCADE,
  CONSTRAINT `watchlist_ibfk_2` FOREIGN KEY (`movie_id`) REFERENCES `movies` (`movie_id`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `watchlist`
--

LOCK TABLES `watchlist` WRITE;
/*!40000 ALTER TABLE `watchlist` DISABLE KEYS */;
INSERT INTO `watchlist` VALUES (2,6,1,'2026-10-26 14:42:58');
/*!40000 ALTER TABLE `watchlist` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2026-10-31 11:42:14
