#

||
|---|
|![Banner](../assets/banner-guide-aws-storage.png)|
||

## TIPOS DE ARMAZENAMENTO

### FILE STORAGE

Historically, operating systems save data in hierarchical file systems organized in the form of directories, sub-directories and files, or folders, sub-folders, and files depending on the operating system.

For example, if you are troubleshooting an issue on a Linux distribution, you may need to look in /var/log or /etc/config. Once inside of these directories, you need to identify which file to explore and open. When using a file-based system, you must know the exact path and location of the files you need to work with or have a way to search the entire structure to find the file you need.  

### BLOCK STORAGE

A block is a range of bytes or bits on a storage device. Block storage files, are divided into blocks and written directly to empty blocks on a physical drive. Each block is assigned a unique identifier and then written to the disk in the most efficient manner possible. Since blocks are assigned identifiers, they do not need to be stored in adjacent sections of the disk. Indeed they can be spread across multiple disks or environments. You can retrieve the individual blocks separately from the rest of the file, which makes block storage excellent for technology like relational databases.

With relational databases, you might only need to retrieve a single piece of a file, such as an inventory tracking number, or one specific employee ID, rather than retrieving the entire inventory listing or whole employee repository.

### OBJECT STORAGE

Unlike the hierarchical structure used in file-based storage, object storage is a flat structure where the data, called an object, is located in a single repository known as a bucket. Object can be organized to imitate a hierarchy by attaching key name prefixes and delimiters. Prefixes and delimiters allow you to group similar items to help visually organize and easily retrieve your data. In the user interface, these prefixes give the appearance of a folder and subfolder structure but in reality, the storage is still a flat structure.

## S3: SIMPLE STORAGE SERVICE

* object storage
* escalabildade
* disponibilidade de dados
* segurança
* performance
* simplicidade & robustez

### RESTRIÇÕES E LIMITAÇÕES

* **Owner**: cada *bucket* é propriedade da conta que o cria, e não pode ser transferido para outras contas
* **Nomes**: os nomes de *bucket* são globalmente únicos, não podem haver duplicações dentro de toda a infraestrutura S3
* **Renomeação**: uma vez criado, não é possível renomear um *bucket*
* **Entidade Permanentes**: *buckets* são entidades de armazenamento permanente e só removíveis quando estão vazios. Após deletar um *bucket*, o nome se torna disponível para reutilização em 24 horas.
* **Limites de Armazenamento de Objetos**: não há limite ao número de objetos a serem armazenados em um *bucket*. No entanto, não é possível criar um *bucket* dentro de um *bucket*, conceito também denominado *nesting buckets*.
* **Limites de Criação de Buckets**: por padrão, é possível criar até 100 *buckets* por conta AWS. Se houver necessidade, é possível aumentar esse limite para até 1000 *buckets*.
* **Tamanho dos Objetos**: cada objeto pode ter até 5 TB.

### REGRAS DE NOMES DE BUCKETS

Your bucket names matter to S3, and based on how you use the bucket, your bucket names and characters will vary. Bucket names are globally viewable and need to be DNS-compliant. 

Here are the rules to follow when naming your buckets. Bucket names must:

* Be unique across all of Amazon S3

* Be between 3-63 characters long

* Consist only of lowercase letters, numbers, dots (.), and hyphens (-)

* Start with a lowercase letter or number

* Not begin with xn-- (beginning February 2020)

* Not be formatted as an IP address. (i.e. 198.68.10.2)

* Use a dot (.) in the name only if the bucket's intended purpose is to host an Amazon S3 static website; otherwise do not use a dot (.) in the bucket name

### OBJETOS

An object consists of the following: Key, version ID, value, metadata, and access control information. The object key (or key name) uniquely identifies the object in a bucket. Object metadata is a set of name-value pairs. You can set object metadata at the time you upload it. After you upload the object, you cannot modify object metadata. The only way to modify object metadata is to make a copy of the object and set the metadata. 

An object is a file and any optional metadata that describes the file. To store a file in Amazon S3, you upload it to a bucket. When you upload a file as an object, you can set permissions on the object and any metadata.

* **Chave | *Key***

```python
            # nome do bucket                       # chave do objeto 
    https://bucket-name.s3-us-west-2.amazonaws.com/pseudopasta/uma_foto.jpg
```

When you create an object, you specify the key name. The key name uniquely identifies the object in the bucket. It is the full path to the object in the bucket.

In Amazon S3, there is no hierarchy, as you would see in a file system. However, by using prefixes and delimiters in an object key name, the Amazon S3 console and the AWS SDKs can infer hierarchy and introduce the concept of folders. You do not get actual folders, what you get is a very long key name.

* **ID de Versão | *Version ID***

Versioning is a means of keeping multiple variants of an object in the same bucket. You can use versioning to preserve, retrieve, and restore every version of every object stored in your Amazon S3 bucket. You can easily recover from both unintended user actions and application failures. If Amazon S3 receives multiple write requests for the same object simultaneously; it stores all of the objects.

* **Valor (ou Tamanho) | *Value (or Size)***

Value (or size) is the actual content that you are storing. An object value can be any sequence of bytes, meaning it can be the whole object or a range of bytes within an object that an application needs to retrieve. Objects can range in size from zero to 5 TB.

* **Metadados** | *Metadata***

For each object stored in a bucket, Amazon S3 maintains a set of system metadata. Amazon S3 processes this system metadata as needed. For example, Amazon S3 maintains object creation date and size metadata and uses this information as part of object management.

There are two categories of system metadata:

- Metadata such as object creation date is system controlled, where only Amazon S3 can modify the value.
- Other system metadata, such as the storage class configured for the object and whether the object has server-side encryption enabled, are examples of system metadata whose values you control.

* **Controle de Acesso | *Access Control***

You can control access to the objects you store in Amazon S3. S3 supports both resource-based and user-based access controls. Access control lists (ACLs) and bucket policies are both examples of resource-based access control.

### TAGS

Amazon S3 tags are key-value pairs and apply to a whole bucket or to individual objects to help with identification, searches, and data classification. Using tags for your objects allows you to effectively manage your storage and provide valuable insight on how your data is used. Newly created tags assigned to a bucket, are not retroactively applied to its existing child objects. 

Adding tags to your objects offer benefits such as the following:

Object tags enable fine-grained access control of permissions. For example, you could grant an IAM user permission to read-only objects with specific tags.
Object tags enable fine-grained object lifecycle management in which you can specify a tag-based filter, in addition to a key name prefix, in a lifecycle rule.
When using Amazon S3 analytics, you can configure filters to group objects together for analysis by object tags, key name prefix, or both prefix and tags.
You can also customize Amazon CloudWatch metrics to display information by specific tag filters. The next lesson provides more details.

* **Tags de Bucket**
Bucket tags allow you to track storage cost, or other criteria, by labeling your Amazon S3 buckets using cost allocation tags. A cost allocation tag is a key-value pair that you associate with an S3 bucket. After you activate cost allocation tags, AWS uses the tags to organize your resource costs on your cost allocation report. You can only use cost allocation tags on buckets and not on individual objects.

AWS provides two types of cost allocation tags, an AWS-generated tag and user-defined tag. AWS defines, creates, and applies the AWS-generated tag, createdBy, for you after an S3 CreateBucket event. You define, create, and apply user-defined tags to your S3 bucket. 

Once you have created and applied the user-defined tags, you can activate them by using the Billing and Cost Management console for cost allocation tracking. Cost Allocation Tags appear on the console after enabling AWS Cost Explorer, AWS Budgets, AWS Cost and Usage reports, or legacy reports. 

Each S3 bucket has a tag set. A tag set contains all of the tags that are assigned to that bucket and can contain as many as 50 tags, or it can be empty. Keys must be unique within a tag set but values don't. 

* **Tags de Objeto**

Object tagging gives you a way to categorize and query your storage. You can add tags to an Amazon S3 object during the upload or after the upload. Each tag is a key-value pair that adheres to the following rules:

You can associate up to 10 tags with an object they must have unique tag keys.
Tag keys can be up to 128 characters in length
Tag values can be up to 255 characters in length
Key and tag values are case sensitive

### REPLICAÇÃO

* **Entre Regiões | *CRR - Cross-Region Replication***

If you need data stored in multiple regions, you can replicate your bucket to other regions using cross-region replication. This enables you to automatically copy objects from a  bucket in one region to different bucket in a another, separate region. You can replicate the entire bucket or you can use tags to replicate only the objects with the tags you choose.

* **Na Mesma Região | *SRR - Same-Region Replication***

Amazon S3 supports automatic and asynchronous replication of newly uploaded S3 objects to a destination bucket in the same AWS Region. 

SRR makes another copy of S3 objects within the same AWS Region, with the same redundancy as the destination storage class. This allows you to automatically aggregate logs from different S3 buckets for in-region processing, or configure live replication between test and development environments. SRR helps you address data sovereignty and compliance requirements by keeping a copy of your objects in the same AWS Region as the original.

### HOSPEDAGEM DE SITE ESTÁTICO

