% order5_0014  eq1=27475 eq2=56080  gold=None
% TRUE-direction: prove eq1 |= eq2
fof(hyp,  axiom,      ! [U,W,X,Y,Z] : ( X = f(f(f(Y,Z),f(W,U)),f(Z,W)) )).
fof(goal, conjecture, ! [W,X,Y,Z] : ( f(X,f(Y,Z)) = f(f(X,X),f(W,Z)) )).
