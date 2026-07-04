% order5_0156  eq1=2122 eq2=38530  gold=None
% TRUE-direction: prove eq1 |= eq2
fof(hyp,  axiom,      ! [W,X,Y,Z] : ( X = f(f(f(Y,X),Z),f(W,W)) )).
fof(goal, conjecture, ! [X,Y,Z] : ( X = f(f(f(Y,f(f(Z,X),X)),Y),X) )).
