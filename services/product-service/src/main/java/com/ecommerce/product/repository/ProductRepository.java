package com.ecommerce.product.repository;

import com.ecommerce.product.model.Product;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.stereotype.Repository;

import java.util.List;
import java.util.Optional;

@Repository
public interface ProductRepository extends JpaRepository<Product, Long> {
    
    List<Product> findByIsActiveTrue();
    
    List<Product> findByCategory(String category);
    
    List<Product> findByCategoryAndIsActiveTrue(String category);
    
    @Query("SELECT p FROM Product p WHERE LOWER(p.name) LIKE LOWER(CONCAT('%', :keyword, '%'))")
    List<Product> searchByName(String keyword);
    
    Optional<Product> findByIdAndIsActiveTrue(Long id);
    
    @Query("SELECT p FROM Product p WHERE p.stock < :threshold AND p.isActive = true")
    List<Product> findLowStockProducts(Integer threshold);
}
