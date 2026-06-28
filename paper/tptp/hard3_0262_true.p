% hard3_0262  eq1=2492 eq2=4149  gold=True
% TRUE-direction: prove eq1 |= eq2
fof(hyp,  axiom,      ! [U,W,X,Y,Z] : ( X = f(f(X,f(f(Y,Z),W)),U) )).
fof(goal, conjecture, ! [W,X,Y,Z] : ( f(X,Y) = f(f(f(X,Z),W),X) )).
