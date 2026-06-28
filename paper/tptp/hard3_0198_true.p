% hard3_0198  eq1=1826 eq2=1410  gold=True
% TRUE-direction: prove eq1 |= eq2
fof(hyp,  axiom,      ! [U,W,X,Y,Z] : ( X = f(f(Y,Z),f(f(W,U),X)) )).
fof(goal, conjecture, ! [W,X,Y,Z] : ( X = f(Y,f(f(f(Z,W),Z),X)) )).
