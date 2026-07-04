% order5v2_0257  eq1=20227 eq2=23986  gold=None
% TRUE-direction: prove eq1 |= eq2
fof(hyp,  axiom,      ! [W,X,Y,Z] : ( X = f(f(Y,Z),f(f(Y,f(Z,Y)),W)) )).
fof(goal, conjecture, ! [U,V,W,X,Y,Z] : ( X = f(f(f(Y,Z),W),f(U,f(V,U))) )).
