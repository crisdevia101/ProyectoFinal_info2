-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Servidor: 127.0.0.1
-- Tiempo de generación: 07-12-2025 a las 19:41:09
-- Versión del servidor: 10.4.32-MariaDB
-- Versión de PHP: 8.2.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Base de datos: `proyecto_info2`
--

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `logs`
--

CREATE TABLE `logs` (
  `id` int(11) NOT NULL,
  `usuario` varchar(100) DEFAULT NULL,
  `fecha` datetime DEFAULT NULL,
  `tipo_actividad` varchar(255) DEFAULT NULL,
  `ruta_archivo` varchar(500) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `logs`
--

INSERT INTO `logs` (`id`, `usuario`, `fecha`, `tipo_actividad`, `ruta_archivo`) VALUES
(2, 'admin', '2025-12-06 22:46:25', 'login', ''),
(3, 'admin', '2025-12-06 22:52:25', 'login', ''),
(4, 'admin', '2025-12-06 22:58:06', 'login', ''),
(5, 'invitado', '2025-12-06 23:01:50', 'login', ''),
(6, 'admin', '2025-12-06 23:24:58', 'login', ''),
(8, 'admin', '2025-12-06 23:30:10', 'login', ''),
(9, 'admin', '2025-12-06 23:30:52', 'captura_foto', 'usuarios\\admin.png'),
(10, 'admin', '2025-12-06 23:40:56', 'login', ''),
(11, 'admin', '2025-12-06 23:46:22', 'login', ''),
(12, 'admin', '2025-12-07 00:00:22', 'login', ''),
(13, 'admin', '2025-12-07 00:03:32', 'login', ''),
(14, 'admin', '2025-12-07 00:08:49', 'login', ''),
(15, 'admin', '2025-12-07 00:11:38', 'login', ''),
(16, 'admin', '2025-12-07 00:33:50', 'login', ''),
(17, 'admin', '2025-12-07 00:49:26', 'login', ''),
(18, 'admin', '2025-12-07 01:03:21', 'login', ''),
(19, 'admin', '2025-12-07 01:10:15', 'login', ''),
(20, 'admin', '2025-12-07 01:14:54', 'login', ''),
(21, 'admin', '2025-12-07 01:22:56', 'login', ''),
(22, 'admin', '2025-12-07 01:30:43', 'login', ''),
(23, 'admin', '2025-12-07 01:33:05', 'login', ''),
(24, 'admin', '2025-12-07 01:34:42', 'login', ''),
(25, 'admin', '2025-12-07 01:35:08', 'cargar_estudio_dicom', 'C:/Users/Cristian Devia/OneDrive - Universidad de Antioquia/Escritorio/Informatica 2/DICOM/DICOM/datos/datos/Sarcoma/img1'),
(26, 'admin', '2025-12-07 01:39:29', 'login', ''),
(27, 'admin', '2025-12-07 01:39:55', 'cargar_estudio_dicom', 'C:/Users/Cristian Devia/OneDrive - Universidad de Antioquia/Escritorio/Informatica 2/DICOM/DICOM/datos/datos/Sarcoma/img1'),
(28, 'admin', '2025-12-07 01:43:42', 'login', ''),
(29, 'admin', '2025-12-07 01:44:03', 'cargar_estudio_dicom', 'C:/Users/Cristian Devia/OneDrive - Universidad de Antioquia/Escritorio/Informatica 2/DICOM/DICOM/datos/datos/Sarcoma/img1'),
(30, 'admin', '2025-12-07 01:46:10', 'login', ''),
(31, 'admin', '2025-12-07 01:46:27', 'cargar_estudio_dicom', 'C:/Users/Cristian Devia/OneDrive - Universidad de Antioquia/Escritorio/Informatica 2/DICOM/DICOM/datos/datos/Sarcoma/img1'),
(32, 'admin', '2025-12-07 01:46:37', 'mip_generada', 'mip_20251207_014637.png'),
(33, 'admin', '2025-12-07 01:49:15', 'login', ''),
(34, 'admin', '2025-12-07 01:49:31', 'cargar_estudio_dicom', 'C:/Users/Cristian Devia/OneDrive - Universidad de Antioquia/Escritorio/Informatica 2/DICOM/DICOM/datos/datos/Sarcoma/img1'),
(35, 'admin', '2025-12-07 09:00:27', 'login', ''),
(36, 'admin', '2025-12-07 09:04:06', 'cargar_estudio_dicom', 'C:/Users/Cristian Devia/OneDrive - Universidad de Antioquia/Escritorio/Informatica 2/DICOM/DICOM/datos/datos/Sarcoma/img1'),
(37, 'admin', '2025-12-07 09:11:49', 'login', ''),
(38, 'admin', '2025-12-07 09:12:09', 'cargar_estudio_dicom', 'C:/Users/Cristian Devia/OneDrive - Universidad de Antioquia/Escritorio/Informatica 2/DICOM/DICOM/datos/datos/Sarcoma/img1'),
(39, 'admin', '2025-12-07 09:15:40', 'login', ''),
(40, 'admin', '2025-12-07 09:16:09', 'cargar_estudio_dicom', 'C:/Users/Cristian Devia/OneDrive - Universidad de Antioquia/Escritorio/Informatica 2/DICOM/DICOM/datos/datos/Sarcoma/img1'),
(41, 'admin', '2025-12-07 09:16:11', 'mip_generada', 'mip_20251207_091611.png'),
(42, 'admin', '2025-12-07 10:51:17', 'login', ''),
(43, 'admin', '2025-12-07 10:53:46', 'login', ''),
(44, 'admin', '2025-12-07 11:04:33', 'login', ''),
(45, 'admin', '2025-12-07 11:13:00', 'login', ''),
(46, 'sistema', '2025-12-07 11:13:14', 'Carga MAT', 'C:/Users/Cristian Devia/OneDrive - Universidad de Antioquia/Escritorio/Informatica 2/StefanyLuna_CristianDevia/E00001.mat'),
(47, 'admin', '2025-12-07 11:15:31', 'login', ''),
(48, 'sistema', '2025-12-07 11:15:40', 'Carga MAT', 'C:/Users/Cristian Devia/OneDrive - Universidad de Antioquia/Escritorio/Informatica 2/StefanyLuna_CristianDevia/E00001.mat'),
(49, 'admin', '2025-12-07 11:20:41', 'login', ''),
(50, 'sistema', '2025-12-07 11:20:55', 'Carga MAT', 'C:/Users/Cristian Devia/OneDrive - Universidad de Antioquia/Escritorio/Informatica 2/StefanyLuna_CristianDevia/E00001.mat'),
(51, 'admin', '2025-12-07 11:23:58', 'login', ''),
(52, 'sistema', '2025-12-07 11:24:08', 'Carga MAT', 'C:/Users/Cristian Devia/OneDrive - Universidad de Antioquia/Escritorio/Informatica 2/StefanyLuna_CristianDevia/E00001.mat'),
(53, 'admin', '2025-12-07 11:29:51', 'login', ''),
(54, 'sistema', '2025-12-07 11:30:08', 'Carga MAT', 'C:/Users/Cristian Devia/OneDrive - Universidad de Antioquia/Escritorio/Informatica 2/StefanyLuna_CristianDevia/senales_potencial.mat'),
(55, 'admin', '2025-12-07 11:32:28', 'login', ''),
(56, 'sistema', '2025-12-07 11:32:41', 'Carga MAT', 'C:/Users/Cristian Devia/OneDrive - Universidad de Antioquia/Escritorio/Informatica 2/StefanyLuna_CristianDevia/senales_potencial.mat'),
(57, 'admin', '2025-12-07 11:36:01', 'login', ''),
(58, 'sistema', '2025-12-07 11:36:19', 'Carga MAT', 'C:/Users/Cristian Devia/OneDrive - Universidad de Antioquia/Escritorio/Informatica 2/StefanyLuna_CristianDevia/E00001.mat'),
(59, 'admin', '2025-12-07 11:45:45', 'login', ''),
(60, 'sistema', '2025-12-07 11:45:57', 'Carga MAT', 'C:/Users/Cristian Devia/OneDrive - Universidad de Antioquia/Escritorio/Informatica 2/StefanyLuna_CristianDevia/E00001.mat'),
(61, 'sistema', '2025-12-07 11:46:35', 'Carga MAT', 'C:/Users/Cristian Devia/OneDrive - Universidad de Antioquia/Escritorio/Informatica 2/StefanyLuna_CristianDevia/parkinson/P007_EP_reposo.mat'),
(62, 'admin', '2025-12-07 11:56:11', 'login', ''),
(63, 'sistema', '2025-12-07 11:56:27', 'Carga MAT', 'C:/Users/Cristian Devia/OneDrive - Universidad de Antioquia/Escritorio/Informatica 2/StefanyLuna_CristianDevia/E00001.mat'),
(64, 'sistema', '2025-12-07 11:56:36', 'Carga MAT', 'C:/Users/Cristian Devia/OneDrive - Universidad de Antioquia/Escritorio/Informatica 2/StefanyLuna_CristianDevia/senales_potencial.mat'),
(65, 'admin', '2025-12-07 11:58:57', 'login', ''),
(66, 'sistema', '2025-12-07 11:59:38', 'Carga MAT', 'C:/Users/Cristian Devia/OneDrive - Universidad de Antioquia/Escritorio/Informatica 2/StefanyLuna_CristianDevia/E00001.mat'),
(67, 'admin', '2025-12-07 12:08:50', 'login', ''),
(68, 'sistema', '2025-12-07 12:09:01', 'Carga MAT', 'C:/Users/Cristian Devia/OneDrive - Universidad de Antioquia/Escritorio/Informatica 2/StefanyLuna_CristianDevia/E00001.mat'),
(69, 'admin', '2025-12-07 12:18:14', 'login', ''),
(70, 'sistema', '2025-12-07 12:18:30', 'Carga MAT', 'C:/Users/Cristian Devia/Downloads/PF_info2/E00001.mat'),
(71, 'admin', '2025-12-07 12:21:05', 'login', ''),
(72, 'sistema', '2025-12-07 12:21:15', 'Carga MAT', 'C:/Users/Cristian Devia/Downloads/PF_info2/E00001.mat'),
(73, 'admin', '2025-12-07 12:22:00', 'captura_foto', 'usuarios\\admin.png'),
(74, 'admin', '2025-12-07 12:29:00', 'login', ''),
(75, 'admin', '2025-12-07 12:32:36', 'login', ''),
(76, 'admin', '2025-12-07 12:38:20', 'login', ''),
(77, 'admin', '2025-12-07 12:40:53', 'login', ''),
(78, 'admin', '2025-12-07 12:44:09', 'login', ''),
(79, 'admin', '2025-12-07 12:44:43', 'cargar_estudio_dicom', 'C:/Users/Cristian Devia/OneDrive - Universidad de Antioquia/Escritorio/Informatica 2/DICOM/DICOM/datos/datos/Sarcoma/img1'),
(80, 'admin', '2025-12-07 12:45:21', 'mip_generada', 'mip_20251207_124521.png'),
(81, 'admin', '2025-12-07 12:47:16', 'login', ''),
(82, 'admin', '2025-12-07 12:47:35', 'cargar_estudio_dicom', 'C:/Users/Cristian Devia/OneDrive - Universidad de Antioquia/Escritorio/Informatica 2/DICOM/DICOM/datos/datos/Sarcoma/img1'),
(83, 'admin', '2025-12-07 12:48:56', 'login', ''),
(84, 'admin', '2025-12-07 12:49:12', 'cargar_estudio_dicom', 'C:/Users/Cristian Devia/OneDrive - Universidad de Antioquia/Escritorio/Informatica 2/DICOM/DICOM/datos/datos/Sarcoma/img2'),
(85, 'admin', '2025-12-07 12:50:12', 'login', ''),
(86, 'admin', '2025-12-07 12:50:37', 'cargar_estudio_dicom', 'C:/Users/Cristian Devia/OneDrive - Universidad de Antioquia/Escritorio/Informatica 2/DICOM/DICOM/datos/datos/Sarcoma/img2'),
(87, 'admin', '2025-12-07 12:50:51', 'mip_generada', 'mip_20251207_125051.png'),
(88, 'sistema', '2025-12-07 12:51:14', 'Carga MAT', 'C:/Users/Cristian Devia/Downloads/PF_info2/E00001.mat'),
(89, 'admin', '2025-12-07 12:57:04', 'login', ''),
(90, 'sistema', '2025-12-07 12:57:12', 'Carga MAT', 'C:/Users/Cristian Devia/Downloads/PF_info2/E00001.mat'),
(91, 'admin', '2025-12-07 13:00:55', 'login', ''),
(92, 'admin', '2025-12-07 13:11:58', 'login', ''),
(93, 'admin', '2025-12-07 13:17:34', 'login', ''),
(94, 'admin', '2025-12-07 13:19:24', 'login', ''),
(95, 'admin', '2025-12-07 13:21:12', 'login', '');

--
-- Índices para tablas volcadas
--

--
-- Indices de la tabla `logs`
--
ALTER TABLE `logs`
  ADD PRIMARY KEY (`id`);

--
-- AUTO_INCREMENT de las tablas volcadas
--

--
-- AUTO_INCREMENT de la tabla `logs`
--
ALTER TABLE `logs`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=96;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
