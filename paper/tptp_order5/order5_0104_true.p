% order5_0104  eq1=15124 eq2=33263  gold=None
% TRUE-direction: prove eq1 |= eq2
fof(hyp,  axiom,      ! [U,W,X,Y,Z] : ( X = f(Y,f(f(f(Z,W),f(Y,U)),X)) )).
fof(goal, conjecture, ! [U,V,W,X,Y,Z] : ( X = f(f(Y,f(f(f(Y,Z),W),U)),V) )).
