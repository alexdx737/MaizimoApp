-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Servidor: 127.0.0.1
-- Tiempo de generación: 07-11-2025 a las 15:14:13
-- Versión del servidor: 10.4.32-MariaDB
-- Versión de PHP: 8.1.25

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Base de datos: `maizimo_app`
--

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `asignacion_tortilla`
--

CREATE TABLE `asignacion_tortilla` (
  `ID_Asignacion` int(11) NOT NULL,
  `ID_Donacion` int(11) NOT NULL,
  `ID_Beneficiario` int(11) NOT NULL,
  `Cantidad_Asignada_Kg` decimal(10,2) NOT NULL,
  `Fecha_Entrega` date NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `beneficiario`
--

CREATE TABLE `beneficiario` (
  `ID_Beneficiario` int(11) NOT NULL,
  `Nombre_Responsable` varchar(100) NOT NULL,
  `Direccion` varchar(255) DEFAULT NULL,
  `Num_Miembros_Familia` int(11) DEFAULT 1,
  `Fecha_Registro` date NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `cliente_mayorista`
--

CREATE TABLE `cliente_mayorista` (
  `ID_Cliente` int(11) NOT NULL,
  `Nombre` varchar(100) NOT NULL,
  `Direccion` varchar(255) DEFAULT NULL,
  `Telefono` varchar(15) DEFAULT NULL,
  `Descuento_Acordado` decimal(5,2) DEFAULT 0.00
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `consumo_insumo`
--

CREATE TABLE `consumo_insumo` (
  `ID_Consumo` int(11) NOT NULL,
  `ID_Venta` int(11) NOT NULL,
  `ID_Insumo` int(11) NOT NULL,
  `Cantidad_Consumida` decimal(10,2) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `detalle_venta`
--

CREATE TABLE `detalle_venta` (
  `ID_Venta` int(11) NOT NULL,
  `ID_Producto` int(11) NOT NULL,
  `Cantidad_Vendida` decimal(10,2) NOT NULL,
  `Subtotal` decimal(10,2) NOT NULL,
  `Uso_Bolsa` tinyint(1) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `donacion`
--

CREATE TABLE `donacion` (
  `ID_Donacion` int(11) NOT NULL,
  `ID_Venta` int(11) NOT NULL,
  `Monto_Redondeo` decimal(5,2) NOT NULL,
  `Monto_En_Tortillas` decimal(10,2) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `empleado`
--

CREATE TABLE `empleado` (
  `ID_Empleado` int(11) NOT NULL,
  `Nombre` varchar(100) NOT NULL,
  `RFC` varchar(13) DEFAULT NULL,
  `Fecha_Contratacion` date DEFAULT NULL,
  `Es_Vulnerable` tinyint(1) NOT NULL DEFAULT 0,
  `Estado_Ciclo` varchar(50) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `insumo`
--

CREATE TABLE `insumo` (
  `ID_Insumo` int(11) NOT NULL,
  `Nombre` varchar(100) NOT NULL,
  `Stock_Actual` decimal(10,2) NOT NULL,
  `Unidad_Medida` varchar(50) NOT NULL,
  `Costo_Unitario` decimal(10,2) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `producto`
--

CREATE TABLE `producto` (
  `ID_Producto` int(11) NOT NULL,
  `Nombre` varchar(100) NOT NULL,
  `Precio_Venta` decimal(10,2) NOT NULL,
  `Unidad_Medida` varchar(50) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `usuario`
--

CREATE TABLE `usuario` (
  `ID_Usuario` int(11) NOT NULL,
  `ID_Empleado` int(11) NOT NULL,
  `Nombre_Usuario` varchar(50) NOT NULL,
  `Contrasena_Hash` varchar(255) NOT NULL,
  `Rol` varchar(50) NOT NULL,
  `Activo` tinyint(1) NOT NULL DEFAULT 1,
  `Fecha_Creacion` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `venta`
--

CREATE TABLE `venta` (
  `ID_Venta` int(11) NOT NULL,
  `Fecha_Hora` datetime NOT NULL,
  `Monto_Total` decimal(10,2) NOT NULL,
  `ID_Cliente_Mayorista` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Índices para tablas volcadas
--

--
-- Indices de la tabla `asignacion_tortilla`
--
ALTER TABLE `asignacion_tortilla`
  ADD PRIMARY KEY (`ID_Asignacion`),
  ADD KEY `ID_Donacion` (`ID_Donacion`),
  ADD KEY `ID_Beneficiario` (`ID_Beneficiario`);

--
-- Indices de la tabla `beneficiario`
--
ALTER TABLE `beneficiario`
  ADD PRIMARY KEY (`ID_Beneficiario`);

--
-- Indices de la tabla `cliente_mayorista`
--
ALTER TABLE `cliente_mayorista`
  ADD PRIMARY KEY (`ID_Cliente`);

--
-- Indices de la tabla `consumo_insumo`
--
ALTER TABLE `consumo_insumo`
  ADD PRIMARY KEY (`ID_Consumo`),
  ADD KEY `ID_Venta` (`ID_Venta`),
  ADD KEY `ID_Insumo` (`ID_Insumo`);

--
-- Indices de la tabla `detalle_venta`
--
ALTER TABLE `detalle_venta`
  ADD PRIMARY KEY (`ID_Venta`,`ID_Producto`),
  ADD KEY `ID_Producto` (`ID_Producto`);

--
-- Indices de la tabla `donacion`
--
ALTER TABLE `donacion`
  ADD PRIMARY KEY (`ID_Donacion`),
  ADD UNIQUE KEY `ID_Venta` (`ID_Venta`);

--
-- Indices de la tabla `empleado`
--
ALTER TABLE `empleado`
  ADD PRIMARY KEY (`ID_Empleado`),
  ADD UNIQUE KEY `RFC` (`RFC`);

--
-- Indices de la tabla `insumo`
--
ALTER TABLE `insumo`
  ADD PRIMARY KEY (`ID_Insumo`);

--
-- Indices de la tabla `producto`
--
ALTER TABLE `producto`
  ADD PRIMARY KEY (`ID_Producto`);

--
-- Indices de la tabla `usuario`
--
ALTER TABLE `usuario`
  ADD PRIMARY KEY (`ID_Usuario`),
  ADD UNIQUE KEY `ID_Empleado` (`ID_Empleado`),
  ADD UNIQUE KEY `Nombre_Usuario` (`Nombre_Usuario`);

--
-- Indices de la tabla `venta`
--
ALTER TABLE `venta`
  ADD PRIMARY KEY (`ID_Venta`),
  ADD KEY `ID_Cliente_Mayorista` (`ID_Cliente_Mayorista`);

--
-- AUTO_INCREMENT de las tablas volcadas
--

--
-- AUTO_INCREMENT de la tabla `asignacion_tortilla`
--
ALTER TABLE `asignacion_tortilla`
  MODIFY `ID_Asignacion` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `beneficiario`
--
ALTER TABLE `beneficiario`
  MODIFY `ID_Beneficiario` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `cliente_mayorista`
--
ALTER TABLE `cliente_mayorista`
  MODIFY `ID_Cliente` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `consumo_insumo`
--
ALTER TABLE `consumo_insumo`
  MODIFY `ID_Consumo` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `donacion`
--
ALTER TABLE `donacion`
  MODIFY `ID_Donacion` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `empleado`
--
ALTER TABLE `empleado`
  MODIFY `ID_Empleado` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `insumo`
--
ALTER TABLE `insumo`
  MODIFY `ID_Insumo` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `producto`
--
ALTER TABLE `producto`
  MODIFY `ID_Producto` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `usuario`
--
ALTER TABLE `usuario`
  MODIFY `ID_Usuario` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `venta`
--
ALTER TABLE `venta`
  MODIFY `ID_Venta` int(11) NOT NULL AUTO_INCREMENT;

--
-- Restricciones para tablas volcadas
--

--
-- Filtros para la tabla `asignacion_tortilla`
--
ALTER TABLE `asignacion_tortilla`
  ADD CONSTRAINT `asignacion_tortilla_ibfk_1` FOREIGN KEY (`ID_Donacion`) REFERENCES `donacion` (`ID_Donacion`),
  ADD CONSTRAINT `asignacion_tortilla_ibfk_2` FOREIGN KEY (`ID_Beneficiario`) REFERENCES `beneficiario` (`ID_Beneficiario`);

--
-- Filtros para la tabla `consumo_insumo`
--
ALTER TABLE `consumo_insumo`
  ADD CONSTRAINT `consumo_insumo_ibfk_1` FOREIGN KEY (`ID_Venta`) REFERENCES `venta` (`ID_Venta`),
  ADD CONSTRAINT `consumo_insumo_ibfk_2` FOREIGN KEY (`ID_Insumo`) REFERENCES `insumo` (`ID_Insumo`);

--
-- Filtros para la tabla `detalle_venta`
--
ALTER TABLE `detalle_venta`
  ADD CONSTRAINT `detalle_venta_ibfk_1` FOREIGN KEY (`ID_Venta`) REFERENCES `venta` (`ID_Venta`),
  ADD CONSTRAINT `detalle_venta_ibfk_2` FOREIGN KEY (`ID_Producto`) REFERENCES `producto` (`ID_Producto`);

--
-- Filtros para la tabla `donacion`
--
ALTER TABLE `donacion`
  ADD CONSTRAINT `donacion_ibfk_1` FOREIGN KEY (`ID_Venta`) REFERENCES `venta` (`ID_Venta`);

--
-- Filtros para la tabla `usuario`
--
ALTER TABLE `usuario`
  ADD CONSTRAINT `usuario_ibfk_1` FOREIGN KEY (`ID_Empleado`) REFERENCES `empleado` (`ID_Empleado`);

--
-- Filtros para la tabla `venta`
--
ALTER TABLE `venta`
  ADD CONSTRAINT `venta_ibfk_1` FOREIGN KEY (`ID_Cliente_Mayorista`) REFERENCES `cliente_mayorista` (`ID_Cliente`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
