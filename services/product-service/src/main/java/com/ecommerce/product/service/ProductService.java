package com.ecommerce.product.service;

import com.ecommerce.product.model.Product;
import com.ecommerce.product.repository.ProductRepository;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.util.List;
import java.util.Optional;

@Service
@RequiredArgsConstructor
@Slf4j
public class ProductService {
    
    private final ProductRepository productRepository;
    
    @Transactional(readOnly = true)
    public List<Product> getAllProducts() {
        log.info("Fetching all active products");
        return productRepository.findByIsActiveTrue();
    }
    
    @Transactional(readOnly = true)
    public Optional<Product> getProductById(Long id) {
        log.info("Fetching product with id: {}", id);
        return productRepository.findByIdAndIsActiveTrue(id);
    }
    
    @Transactional(readOnly = true)
    public List<Product> getProductsByCategory(String category) {
        log.info("Fetching products for category: {}", category);
        return productRepository.findByCategoryAndIsActiveTrue(category);
    }
    
    @Transactional(readOnly = true)
    public List<Product> searchProducts(String keyword) {
        log.info("Searching products with keyword: {}", keyword);
        return productRepository.searchByName(keyword);
    }
    
    @Transactional
    public Product createProduct(Product product) {
        log.info("Creating new product: {}", product.getName());
        product.setIsActive(true);
        return productRepository.save(product);
    }
    
    @Transactional
    public Product updateProduct(Long id, Product productDetails) {
        log.info("Updating product with id: {}", id);
        return productRepository.findById(id)
            .map(product -> {
                product.setName(productDetails.getName());
                product.setDescription(productDetails.getDescription());
                product.setPrice(productDetails.getPrice());
                product.setStock(productDetails.getStock());
                product.setCategory(productDetails.getCategory());
                product.setImageUrl(productDetails.getImageUrl());
                return productRepository.save(product);
            })
            .orElseThrow(() -> new RuntimeException("Product not found with id: " + id));
    }
    
    @Transactional
    public void deleteProduct(Long id) {
        log.info("Soft deleting product with id: {}", id);
        productRepository.findById(id)
            .ifPresent(product -> {
                product.setIsActive(false);
                productRepository.save(product);
            });
    }
    
    @Transactional
    public void updateStock(Long id, Integer quantity) {
        log.info("Updating stock for product id: {} with quantity: {}", id, quantity);
        productRepository.findById(id)
            .ifPresent(product -> {
                product.setStock(product.getStock() + quantity);
                productRepository.save(product);
            });
    }
    
    @Transactional(readOnly = true)
    public List<Product> getLowStockProducts(Integer threshold) {
        log.info("Fetching products with stock below: {}", threshold);
        return productRepository.findLowStockProducts(threshold);
    }
}
