% order5v2_1403  eq1=6031 eq2=17812  gold=None
% TRUE-direction: prove eq1 |= eq2
fof(hyp,  axiom,      ! [W,X,Y,Z] : ( X = f(Y,f(Y,f(Z,f(f(Y,W),Z)))) )).
fof(goal, conjecture, ! [U,V,W,X,Y,Z] : ( X = f(f(Y,Z),f(W,f(W,f(U,V)))) )).
