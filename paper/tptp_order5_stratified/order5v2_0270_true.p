% order5v2_0270  eq1=17847 eq2=19691  gold=None
% TRUE-direction: prove eq1 |= eq2
fof(hyp,  axiom,      ! [U,V,W,X,Y,Z] : ( X = f(f(Y,Z),f(W,f(U,f(V,U)))) )).
fof(goal, conjecture, ! [W,X,Y,Z] : ( X = f(f(X,Y),f(f(X,f(Z,W)),W)) )).
