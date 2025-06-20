
## 问题一

- 题目标题：部门最高工资查询

- 建表语句：
```sql
CREATE TABLE employees (
    id INT PRIMARY KEY,
    name VARCHAR(50),
    department_id INT,
    salary DECIMAL(10, 2)
);
```

- 题目描述：
编写 SQL 查询，找出每个部门的最高工资。结果应包含部门 ID 和对应的最高工资，按部门 ID 升序排列。

- 输入示例：

| id | name  | department_id | salary |
|----|-------|---------------|--------|
| 1  | Alice | 101           | 5000   |
| 2  | Bob   | 101           | 6000   |
| 3  | Carol | 102           | 5500   |
| 4  | Dave  | 102           | 5500   |

- 输出示例：

| department_id | max_salary |
|---------------|------------|
| 101           | 6000.00    |
| 102           | 5500.00    |

-   测试点1
    -   输入数据
    ```sql
    INSERT INTO employees VALUES
    (1, 'Alice', 101, 5000.00),
    (2, 'Bob', 101, 6000.00),
    (3, 'Carol', 102, 5500.00);
    ```
    -   标准输出
    ```text
    [(101, 6000.00), (102, 5500.00)]
    ```

-   测试点2
    -   输入数据
    ```sql
    INSERT INTO employees VALUES
    (4, 'Dave', 103, 4500.00),
    (5, 'Eve', 103, 4500.00),
    (6, 'Frank', 104, 7000.00);
    ```
    -   标准输出
    ```text
    [(103, 4500.00), (104, 7000.00)]
    ```

##  问题二

- 题目标题：用户订单统计

- 建表语句：
```sql
CREATE TABLE users (
    user_id INT PRIMARY KEY,
    username VARCHAR(50)
);

CREATE TABLE orders (
    order_id INT PRIMARY KEY,
    user_id INT,
    order_date DATE,
    FOREIGN KEY (user_id) REFERENCES users(user_id)
);
```

- 题目描述：
编写 SQL 查询，统计每个用户的订单数量（包括没有订单的用户）。结果应包含用户名和对应的订单数量，按订单数量降序排列，若数量相同则按用户名升序排列。

- 输入示例：

users表：

| user_id | username |
|---------|----------|
| 1       | Alice    |
| 2       | Bob      |
| 3       | Carol    |

orders表：

| order_id | user_id | order_date |
|----------|---------|------------|
| 101      | 1       | 2023-01-01 |
| 102      | 1       | 2023-01-05 |
| 103      | 2       | 2023-01-10 |

- 输出示例：

| username | order_count |
|----------|-------------|
| Alice    | 2           |
| Bob      | 1           |
| Carol    | 0           |

-   测试点1
    -   输入数据
    ```sql
    INSERT INTO users VALUES
    (1, 'Alice'),
    (2, 'Bob'),
    (3, 'Carol');

    INSERT INTO orders VALUES
    (101, 1, '2023-01-01'),
    (102, 2, '2023-01-02'),
    (103, 2, '2023-01-03');
    ```
    -   标准输出
    ```text
    [('Bob', 2), ('Alice', 1), ('Carol', 0)]
    ```

-   测试点2
    -   输入数据
    ```sql
    INSERT INTO users VALUES
    (4, 'Dave'),
    (5, 'Eve');

    INSERT INTO orders VALUES
    (104, 4, '2023-01-04'),
    (105, 4, '2023-01-05'),
    (106, 5, '2023-01-06'),
    (107, 5, '2023-01-07');
    ```
    -   标准输出
    ```text
    [('Dave', 2), ('Eve', 2)]
    ```

##  问题三

- 题目标题：连续出现的数字

- 建表语句：
```sql
CREATE TABLE logs (
    id INT PRIMARY KEY,
    num INT
);
```

- 题目描述：
编写 SQL 查询，找出至少连续出现三次的数字。结果应只包含满足条件的数字，且不重复。

- 输入示例：

| id | num |
|----|-----|
| 1  | 1   |
| 2  | 1   |
| 3  | 1   |
| 4  | 2   |
| 5  | 2   |
| 6  | 2   |
| 7  | 2   |
| 8  | 3   |
| 9  | 3   |
| 10 | 4   |

- 输出示例：

| ConsecutiveNums |
|-----------------|
| 1              |
| 2              |

-   测试点1
    -   输入数据
    ```sql
    INSERT INTO logs VALUES
    (1, 1),
    (2, 1),
    (3, 1),
    (4, 2),
    (5, 2),
    (6, 3);
    ```
    -   标准输出
    ```text
    [(1,)]
    ```

-   测试点2
    -   输入数据
    ```sql
    INSERT INTO logs VALUES
    (1, 5),
    (2, 5),
    (3, 5),
    (4, 5),
    (5, 6),
    (6, 6),
    (7, 6),
    (8, 7),
    (9, 7);
    ```
    -   标准输出
    ```text
    [(5,), (6,)]
    ```

-   50分代码
```sql
SELECT l1.num AS ConsecutiveNums
FROM logs l1
JOIN logs l2 ON l1.id + 1 = l2.id AND l1.num = l2.num
JOIN logs l3 ON l1.id + 2 = l3.id AND l1.num = l3.num;
```

-   100分代码
```sql
SELECT DISTINCT l1.num AS ConsecutiveNums
FROM logs l1
JOIN logs l2 ON l1.id + 1 = l2.id AND l1.num = l2.num
JOIN logs l3 ON l1.id + 2 = l3.id AND l1.num = l3.num;
```