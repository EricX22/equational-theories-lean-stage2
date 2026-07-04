% order5v2_0387  eq1=32385 eq2=42470  gold=None
% TRUE-direction: prove eq1 |= eq2
fof(hyp,  axiom,      ! [U,W,X,Y,Z] : ( X = f(f(Y,f(f(Y,f(Z,W)),U)),U) )).
fof(goal, conjecture, ! [X,Y,Z] : ( f(X,X) = f(Y,f(X,f(f(Y,X),Z))) )).
