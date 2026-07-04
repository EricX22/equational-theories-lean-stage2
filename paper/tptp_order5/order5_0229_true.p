% order5_0229  eq1=21693 eq2=42736  gold=None
% TRUE-direction: prove eq1 |= eq2
fof(hyp,  axiom,      ! [W,X,Y,Z] : ( X = f(f(Y,f(X,Z)),f(W,f(Y,Z))) )).
fof(goal, conjecture, ! [W,X,Y,Z] : ( f(X,Y) = f(X,f(Z,f(f(W,X),Z))) )).
