% order5v2_0037  eq1=29192 eq2=6857  gold=None
% TRUE-direction: prove eq1 |= eq2
fof(hyp,  axiom,      ! [U,W,X,Y,Z] : ( X = f(f(f(f(Y,Z),W),W),f(X,U)) )).
fof(goal, conjecture, ! [X,Y,Z] : ( X = f(Y,f(Y,f(f(Y,Y),f(Z,Y)))) )).
