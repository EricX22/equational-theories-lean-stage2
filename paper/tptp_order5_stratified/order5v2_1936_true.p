% order5v2_1936  eq1=6293 eq2=14092  gold=None
% TRUE-direction: prove eq1 |= eq2
fof(hyp,  axiom,      ! [W,X,Y,Z] : ( X = f(Y,f(Z,f(Z,f(f(W,Z),Y)))) )).
fof(goal, conjecture, ! [W,X,Y,Z] : ( X = f(Y,f(f(Z,f(f(Y,Z),Z)),W)) )).
