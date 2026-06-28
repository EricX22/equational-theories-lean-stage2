% hard3_0261  eq1=2483 eq2=1461  gold=True
% TRUE-direction: prove eq1 |= eq2
fof(hyp,  axiom,      ! [W,X,Y,Z] : ( X = f(f(X,f(f(Y,Z),Y)),W) )).
fof(goal, conjecture, ! [X,Y,Z] : ( X = f(f(X,Y),f(Z,f(X,X))) )).
