% order5v2_0550  eq1=38895 eq2=29431  gold=None
% TRUE-direction: prove eq1 |= eq2
fof(hyp,  axiom,      ! [U,V,W,X,Y,Z] : ( X = f(f(f(Y,f(f(Z,W),U)),V),U) )).
fof(goal, conjecture, ! [W,X,Y,Z] : ( X = f(f(X,f(Y,f(Z,f(W,X)))),W) )).
