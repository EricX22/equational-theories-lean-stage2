% order5v2_1275  eq1=5539 eq2=28949  gold=None
% TRUE-direction: prove eq1 |= eq2
fof(hyp,  axiom,      ! [U,W,X,Y,Z] : ( X = f(Y,f(Z,f(W,f(U,f(X,U))))) )).
fof(goal, conjecture, ! [U,W,X,Y,Z] : ( X = f(f(f(f(Y,Z),X),W),f(W,U)) )).
