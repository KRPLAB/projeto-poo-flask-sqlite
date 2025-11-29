# Arquitetura e Modelagem Orientada a Objetos com Python para sistema de monitoramento de gás (ESP32)

## Introdução ao Projeto

Este projeto é desenvolvido como parte da **avaliação bimestral** para as disciplinas de Introdução a Sistemas Embarcados e Programação Orientada a Objeto. O objetivo principal é aplicar a metodologia de desenvolvimento de sistemas embarcados para criar a **especificação funcional, técnica e lógica** completa de um dispositivo que **resolve um problema real** e aplicando também conhecimentos das disciplinas de Programação Orientada a Objetos e Banco de Dados I, aplicando as tecnologias e fundamentos aprendidos nestas disciplinas.

O problema real escolhido é o perigo de vazamentos de Gás Liquefeito de Petróleo (GLP) em ambientes residenciais, que podem não ser detectados a tempo e causar asfixia, incêndios ou explosões.

Como solução, este documento especifica um sistema de monitoramento e alerta baseado no **ESP32**. O sistema utiliza um sensor de gás da série MQ para identificar concentrações perigosas, aciona alertas locais imediatos (sonoros/visuais) e transmite notificações remotas via protocolo MQTT sobre uma rede Wi-Fi.O sistema proposto monitora leituras de sensores de gás, registra-as em banco local (SQLite) e fornece uma API REST (Flask) para consulta e geração de alertas. A modelagem orientada a objetos separa claramente responsabilidades: modelos (representam o domínio), DAOs (persistência) e controladores/rotas (interface). Essa separação facilita manutenção, testes e evolução do sistema. Para o projeto, pensando em **Programação Orientada a Objetos (POO)** e **integração com banco de dados** (SQLite ou MySQL), definiremos um conjunto de **entidades (classes)** que fazem muito sentido no domínio do problema do sensor de gás que envia alertas e leituras via MQTT.

## Fundamentos e decisões de projeto

POO: Cada entidade do domínio é modelada como uma classe que encapsula dados e métodos relevantes. Ex.: Leitura tem método e_perigosa() para lógica de negócio.

Separação de camadas: (1) Models/DAOs — responsabilidade de persistência; (2) Controllers/Flask — responsabilidade de exposição da API e regras de entrada/saída.

SQLite: Escolhido pela simplicidade, portabilidade e por ser suficiente para protótipos e trabalhos acadêmicos. Utilização local (arquivo database.db) reduz complexidade operativa.

DAOs: Facilitam a troca de implementação do banco (por exemplo, migrar para PostgreSQL no futuro) mantendo a API das classes inalterada.

Transações e integridade: Uso de PRAGMA foreign_keys = ON e chave estrangeira para garantir integridade referencial entre sensores e leituras.

Teste e reprodutibilidade: Scripts SQL (schema) e métodos criar_tabela() nos DAOs permitem inicializar ambiente em qualquer máquina.

### Entidades

1. **Sensor**

Representa o sensor físico (ex.: MQ-2 ou MQ-5).

**Atributos:**

* `id`
* `tipo` (MQ2, MQ5…)
* `localizacao` (cozinha, área de serviço…)
* `status` (ativo/inativo)

**Métodos:**

* `ativar()`
* `desativar()`
* `registrar_leitura(valor)`

**BD:** tabela `sensores`

---

2. **Leitura**

Cada leitura enviada pelo ESP32 via MQTT.

**Atributos:**

* `id`
* `sensor_id`
* `valor`
* `data_hora`

**Métodos:**

* `é_perigosa()` → retorna True se valor supera limite

**BD:** tabela `leituras`

---

3. **Alarme / Notificação**

Quando o valor do gás ultrapassa o limite, um alerta é gerado.

**Atributos:**

* `id`
* `sensor_id`
* `nivel` (baixo/médio/alto)
* `mensagem`
* `data_hora`

**Métodos:**

* `enviar_para_app()`
* `marcar_como_resolvido()`

**BD:** tabela `alertas`

---

4. **Dispositivo**

Representa o próprio ESP32.

**Atributos:**

* `id`
* `mac_address`
* `descricao`
* `status` (online/offline)

**Métodos:**

* `conectar()`
* `desconectar()`
* `publicar_mensagem()`

**BD:** tabela `dispositivos`

---


### **Fluxo POO dentro do projeto**

Quando o ESP32 manda `"sensor/gas/cozinha"` com valor:

1. O Flask recebe via MQTT → aciona classe `Sensor`.
2. Cria um objeto `Leitura(valor, sensor_id)`.
3. Se `leitura.é_perigosa()` → cria objeto `Alarme`.
4. `Alarme.enviar_para_app()` (notificação push ou app consumindo API).
5. Tudo é gravado no SQLite/MySQL via classes DAO ou Repositórios.

---

### **Estrutura de pastas completa de POO**

```
/models
  sensor.py
  leitura.py
  dispositivo.py
  alarme.py
  usuario.py

/database
  conexao.py
  sensor_dao.py
  leitura_dao.py
  alarme_dao.py

/routes
  sensores.py
  leituras.py
  alertas.py
  dispositivos.py

/services
  sensor_service.py
  leitura_service.py
  alerta_service.py
  dispositivo_service.py

/mqtt
  cliente_mqtt.py

/app.py (Flask)
```

---

### **Fundamentos do porque essas entidades funcionam bem para POO?**

* Cada classe representa **algo real no sistema** (boa modelagem de domínio).
* Permite manipular objetos no código e persistir no banco (ORM ou DAO).
* Ajuda a separar responsabilidades (princípio SOLID).
* É fácil de demonstrar no trabalho para o professor.

---

### **Diagrama de CLasses UML de modelo classe**

![diagrama UML de ](./diagramaUML.svg "a title")
---

