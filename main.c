

tnode *stack[10];
int top =
-1;
void push(tnode *op) {
stack[++top]=op;
}
tnode* pop() {
return(stack[top--]);
}
void create(char postfix[]) {
tnode*newnode;
int i ;
for(
i=0;postfix[i]!='\0';i++)
{
newnode = (tnode*)malloc(sizeof(tnode));
newnode->left=newnode->right = NULL;
newnode->info = postfix[i];
if(isalpha(postfix[i]))
push(newnode);
else {
newnode->right = pop();
newnode->left = pop();
push(newnode);
}
}
root = pop();
}
void inorder(tnode *root)
{
if(root!=NULL) {
inorder(root->left);
printf("%c ",root->info);
inorder(root->right);
}
}
void postorder
(tnode *root)
{
if(root!=NULL) {
postorder(root
->left);
postorder(root
->right);
printf("%c ",root
->info);
}
}
void preorder(tnode *root) {
if(root!=NULL) {
printf("%c ",root
->info);
preorder(root
->left);
preorder(root
->right);
}
}
int main( ) {
char postfix[20];
printf("Enter the postfix
expression:");
scanf("%s",postfix);
create(postfix);
printf("
\n");
inorder(root);
printf("
\n");
postorder(root);
printf("
\n");
preorder(root);
getch();
}
