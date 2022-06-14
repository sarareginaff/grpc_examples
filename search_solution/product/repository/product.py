from pb.product_pb2 import Product

def _populate_database():
    return [
        Product(
            sku="79756",
            name="Sabonete em Barra Nativa SPA Karité 2 unidades de 90g",
            images = Product.Images(
                                    small="https://res.cloudinary.com/beleza-na-web/image/upload/w_297,f_auto,fl_progressive,q_auto:eco,w_80/v1/imagens/products/B79756/79756-b.jpg", 
                                    large="https://res.cloudinary.com/beleza-na-web/image/upload/w_297,f_auto,fl_progressive,q_auto:eco,w_80/v1/imagens/products/B79756/79756-c.jpg"
                                    )
        ),
        Product(
            sku="72501",
            name="Desodorante Antitranspirante Roll-On Capricho 55ml",
            images = Product.Images(
                                    small="https://res.cloudinary.com/beleza-na-web/image/upload/w_297,f_auto,fl_progressive,q_auto:eco,w_80/v1/imagens/product/B72501/a2a72db3-7ef6-436f-9702-56f56b9329f7-desodorante-antitranspirante-roll-on-capricho-55ml.png"
                                    )
        ),
        Product(
            sku="76599",
            name="Lápis Batom Instalip Mate Vermelho Intense 1,2g",
            images = Product.Images(
                                    small="https://res.cloudinary.com/beleza-na-web/image/upload/w_297,f_auto,fl_progressive,q_auto:eco,w_80/v1/imagens/products/B76599/Slide4.JPG", 
                                    large="https://res.cloudinary.com/beleza-na-web/image/upload/w_297,f_auto,fl_progressive,q_auto:eco,w_80/v1/imagens/products/B76599/VEREMLEHO.jpg"
                                    )
        ),
        Product(
            sku="72038",
            name="Brilho Labial Rose Glitter Capricho, 5,6ml",
            images = Product.Images(
                                    small="https://res.cloudinary.com/beleza-na-web/image/upload/w_297,f_auto,fl_progressive,q_auto:eco,w_80/v1/imagens/product/B72038/0f83194e-b414-4dad-8815-65fad2026496-capricho-brilho-labial-72037-p.png", 
                                    large="https://res.cloudinary.com/beleza-na-web/image/upload/w_297,f_auto,fl_progressive,q_auto:eco,w_80/v1/imagens/product/B72038/e8887b5f-a459-43bb-a757-7aa3099eb3d6-capricho-brilho-labial-72037-p.png"
                                    )
        ),
        Product(
            sku="83599",
            name="Sombra Mate Compacta Amarela pra deixar o dia feliz Intense by Manu Gavassi",
            images = Product.Images(
                                    small="https://res.cloudinary.com/beleza-na-web/image/upload/w_297,f_auto,fl_progressive,q_auto:eco,w_80/v1/imagens/products/B83599/Slide20.JPG", 
                                    large="https://res.cloudinary.com/beleza-na-web/image/upload/w_297,f_auto,fl_progressive,q_auto:eco,w_80/v1/imagens/products/B83599/Slide22.JPG"
                                    )
        ),
        Product(
            sku="83600",
            name="Sombra Mate Compacta Azul pra meditar Intense by Manu Gavassi",
            images = Product.Images(
                                    small="https://res.cloudinary.com/beleza-na-web/image/upload/w_297,f_auto,fl_progressive,q_auto:eco,w_80/v1/imagens/products/B83600/Slide23.JPG", 
                                    large="https://res.cloudinary.com/beleza-na-web/image/upload/w_297,f_auto,fl_progressive,q_auto:eco,w_80/v1/imagens/products/B83600/Slide24.JPG"
                                    )
        ),
        Product(
            sku="83597",
            name="Sombra Mate Compacta Coral pra construir seu império Intense by Manu Gavassi",
            images = Product.Images(
                                    small="https://res.cloudinary.com/beleza-na-web/image/upload/w_297,f_auto,fl_progressive,q_auto:eco,w_80/v1/imagens/products/B83597/Slide17.JPG", 
                                    large="https://res.cloudinary.com/beleza-na-web/image/upload/w_297,f_auto,fl_progressive,q_auto:eco,w_80/v1/imagens/products/B83597/Slide19.JPG"
                                    )
        ),
        Product(
            sku="80423",
            name="Sabonete Em Barra Quinteto Cuide-Se Bem Deleite, 5 Unidades De 80 g Cada",
            images = Product.Images(
                                    small="https://res.cloudinary.com/beleza-na-web/image/upload/w_297,f_auto,fl_progressive,q_auto:eco,w_80/v1/imagens/product/B80423/465f844a-52d2-4c2e-9fad-9d07ceb0d428-sabonete-em-barra-quinteto-cuide-se-bem-deleite-5-unidades-de-80-g-cada.png"
                                    )
        ),
        Product(
            sku="81480",
            name="Lápis para Sobrancelhas #1 Intense 1,1g",
            images = Product.Images(
                                    small="https://res.cloudinary.com/beleza-na-web/image/upload/w_297,f_auto,fl_progressive,q_auto:eco,w_80/v1/imagens/products/B81480/Slide2.JPG", 
                                    large="https://res.cloudinary.com/beleza-na-web/image/upload/w_297,f_auto,fl_progressive,q_auto:eco,w_80/v1/imagens/products/B81480/Slide3.JPG"
                                    )
        ),
        Product(
            sku="83595",
            name="Delineador Líquido para Olhos Azul Hipnose Intense by Manu Gavassi",
            images = Product.Images(
                                    small="https://res.cloudinary.com/beleza-na-web/image/upload/w_297,f_auto,fl_progressive,q_auto:eco,w_80/v1/imagens/products/B83595/Slide3.JPG", 
                                    large="https://res.cloudinary.com/beleza-na-web/image/upload/w_297,f_auto,fl_progressive,q_auto:eco,w_80/v1/imagens/products/B83595/BT_03_21_83596_cartucho.0001.jpg"
                                    )
        ),
        Product(
            sku="81359",
            name="Kit Presente Cuide-se Bem para Mãos: Leite & Mel 30ml + Rosa & Algodão 30ml",
            images = Product.Images(
                                    small="https://res.cloudinary.com/beleza-na-web/image/upload/w_297,f_auto,fl_progressive,q_auto:eco,w_80/v1/imagens/products/B81359/frento", 
                                    large="https://res.cloudinary.com/beleza-na-web/image/upload/w_297,f_auto,fl_progressive,q_auto:eco,w_80/v1/imagens/products/B81359/81359_2.png"
                                    )
        )
    ]

class ProductRepository:
    _database = _populate_database()
  
    def GetProductDataByTerm(self, term: str) -> list:
        products = [p for p in self._database if term.lower() in p.name.lower()]
        return products

    def GetProductDataBySkus(self, skus: str) -> list:
        products = [p for p in self._database if p.sku in skus]
        return products
