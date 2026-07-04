% order5_0184  eq1=51037 eq2=36206  gold=None
% TRUE-direction: prove eq1 |= eq2
fof(hyp,  axiom,      ! [W,X,Y,Z] : ( f(X,Y) = f(f(Z,f(f(W,X),X)),Z) )).
fof(goal, conjecture, ! [W,X,Y,Z] : ( X = f(f(f(Y,f(Z,W)),f(W,X)),Z) )).
