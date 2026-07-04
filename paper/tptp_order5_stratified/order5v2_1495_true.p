% order5v2_1495  eq1=17799 eq2=52840  gold=None
% TRUE-direction: prove eq1 |= eq2
fof(hyp,  axiom,      ! [W,X,Y,Z] : ( X = f(f(Y,Z),f(W,f(W,f(Z,Z)))) )).
fof(goal, conjecture, ! [U,V,W,X,Y,Z] : ( f(X,Y) = f(f(f(Z,f(W,Y)),U),V) )).
